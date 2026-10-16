import asyncio
import logging
from datetime import date

from fastapi import Depends

from src.model import JevQuestions, MindcaseJob, PageModel, ScarapperModel
from src.service.jev.jevService import JevService
from src.service.jev.prompts.prompts import NOUL_PROMPT
from src.service.mindcase.mindcaseService import MindcaseService
from src.service.mindcase.util.jobBuilders import POSTS_NEWER_THAN
from src.service.openai.openaiService import OpenAiService
from src.service.opensearch.opensearch import OpenSearch

logger = logging.getLogger(__name__)
backgroundTasks: set[asyncio.Task] = set()


class AppService:
    mindcaseService: MindcaseService
    openAiService: OpenAiService
    jevService: JevService
    openSearch: OpenSearch

    def __init__(
        self,
        mindcaseService: MindcaseService = Depends(MindcaseService),
        openAiService: OpenAiService = Depends(OpenAiService),
        jevService: JevService = Depends(JevService),
        openSearch: OpenSearch = Depends(OpenSearch),
    ):
        self.mindcaseService = mindcaseService
        self.openAiService = openAiService
        self.jevService = jevService
        self.openSearch = openSearch

    async def scrapeGroups(self, request: ScarapperModel):
        print(f"[app] prompt: {request.prompt}")
        parsed = await self.openAiService.parsePrompt(request.prompt)
        sources = parsed.toSources()
        print(f"[openai] sources: { {platform.name: targets for platform, targets in sources.items()} }")
        print(f"[openai] filters: {parsed.filters}")
        questions = self.jevService.buildNoulQuestions(parsed.filters, NOUL_PROMPT)
        jobs = self.mindcaseService.buildJobs(sources)
        print(f"[app] {len(jobs)} jobs, jev questions: {list(questions)}")
        result = await self.processJobs(jobs, questions)
        print(f"[app] done: {result['posts']} posts, {len(result['validPosts'])} valid, {len(result['failed'])} failed jobs, {len(result['failedPosts'])} failed posts, cached {result['cached']}")
        return {
            "sources": {platform.name: targets for platform, targets in sources.items()},
            "filters": parsed.filters,
            **result,
        }

    async def processJobs(self, jobs: list[MindcaseJob], questions: JevQuestions):
        scrapeTasks = {asyncio.create_task(self.fetchPosts(job)): job for job in jobs}

        seenPostIds: set[tuple[str, str]] = set()
        validPosts: list[PageModel] = []
        failed: dict[str, str] = {}
        failedPosts: dict[str, str] = {}
        uploadTasks: list[asyncio.Task] = []
        cached: list[str] = []
        async for task in asyncio.as_completed(scrapeTasks):
            job = scrapeTasks[task]
            if task.exception():
                failed[f"{job.platform.name}:{job.target}"] = str(task.exception())
                print(f"[app] {job.platform.name}:{job.target} FAILED: {task.exception()}")
                continue

            posts, fromCache = task.result()
            if fromCache:
                cached.append(f"{job.platform.name}:{job.target}")
            else:
                uploadTasks.append(self.runInBackground(self.saveToOpenSearch(job, posts)))
            newPosts: list[PageModel] = []
            for post in posts:
                key = (job.platform.name, post.postId)
                if key not in seenPostIds:
                    seenPostIds.add(key)
                    newPosts.append(post)
            print(f"[app] {job.platform.name}:{job.target} sending {len(newPosts)} posts to jev")
            passed, jevFailed = await self.jevService.extractPostData(newPosts, questions)
            print(f"[jev] {job.platform.name}:{job.target} {len(passed)} passed, {len(jevFailed)} failed")
            validPosts.extend(passed)
            failedPosts.update(jevFailed)

        self.runInBackground(self.closeOpenSearch(uploadTasks))
        return {
            "questions": list(questions.keys()),
            "posts": len(seenPostIds),
            "validPosts": validPosts,
            "failed": failed,
            "failedPosts": failedPosts,
            "cached": cached,
        }

    def runInBackground(self, coroutine) -> asyncio.Task:
        task = asyncio.create_task(coroutine)
        backgroundTasks.add(task)
        task.add_done_callback(backgroundTasks.discard)
        return task

    async def fetchPosts(self, job: MindcaseJob) -> tuple[list[PageModel], bool]:
        try:
            cachedPosts = await self.openSearch.getDocuments(date.fromisoformat(POSTS_NEWER_THAN), job.target, job.platform)
            if cachedPosts:
                print(f"[cache] {job.platform.name}:{job.target} hit, {len(cachedPosts)} posts")
                return cachedPosts, True
            print(f"[cache] {job.platform.name}:{job.target} miss, calling mindcase")
        except Exception:
            logger.exception(f"opensearch read failed for {job.platform.name}:{job.target}")
        return await self.mindcaseService.runJob(job), False

    async def saveToOpenSearch(self, job: MindcaseJob, posts: list[PageModel]):
        try:
            uploaded = await self.openSearch.bulkUpload(job.platform, posts)
            print(f"[opensearch] {job.platform.name}:{job.target} saved {uploaded} posts")
        except Exception:
            logger.exception(f"opensearch upload failed for {job.platform.name}:{job.target}, {len(posts)} posts")

    async def closeOpenSearch(self, uploadTasks: list[asyncio.Task]):
        await asyncio.gather(*uploadTasks)
        try:
            await self.openSearch.close()
        except Exception:
            logger.exception("opensearch close failed")
