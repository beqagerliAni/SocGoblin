import asyncio

from fastapi import Depends

from src.model import JevQuestions, MindcaseJob, PageModel, ScarapperModel
from src.service.jev.jevService import JevService
from src.service.jev.prompts.prompts import NOUL_PROMPT
from src.service.mindcase.mindcaseService import MindcaseService
from src.service.openai.openaiService import OpenAiService


class AppService:
    mindcaseService: MindcaseService
    openAiService: OpenAiService
    jevService: JevService

    def __init__(
        self,
        mindcaseService: MindcaseService = Depends(MindcaseService),
        openAiService: OpenAiService = Depends(OpenAiService),
        jevService: JevService = Depends(JevService),
    ):
        self.mindcaseService = mindcaseService
        self.openAiService = openAiService
        self.jevService = jevService

    async def scrapeGroups(self, request: ScarapperModel):
        parsed = await self.openAiService.parsePrompt(request.prompt)
        sources = parsed.toSources()
        questions = self.jevService.buildNoulQuestions(parsed.filters, NOUL_PROMPT)
        jobs = self.mindcaseService.buildJobs(sources)
        result = await self.processJobs(jobs, questions)
        return {
            "sources": {platform.name: targets for platform, targets in sources.items()},
            "filters": parsed.filters,
            **result,
        }

    async def processJobs(self, jobs: list[MindcaseJob], questions: JevQuestions):
        scrapeTasks = {asyncio.create_task(self.mindcaseService.runJob(job)): job for job in jobs}

        seenPostIds: set[tuple[str, str]] = set()
        validPosts: list[PageModel] = []
        failed: dict[str, str] = {}
        failedPosts: dict[str, str] = {}
        async for task in asyncio.as_completed(scrapeTasks):
            job = scrapeTasks[task]
            if task.exception():
                failed[f"{job.platform.name}:{job.target}"] = str(task.exception())
                continue
            
            newPosts: list[PageModel] = []
            for post in task.result():
                key = (job.platform.name, post.postId)
                if key not in seenPostIds:
                    seenPostIds.add(key)
                    newPosts.append(post)
            passed, jevFailed = await self.jevService.extractPostData(newPosts, questions)
            validPosts.extend(passed)
            failedPosts.update(jevFailed)

        return {
            "questions": list(questions.keys()),
            "posts": len(seenPostIds),
            "validPosts": validPosts,
            "failed": failed,
            "failedPosts": failedPosts,
        }
