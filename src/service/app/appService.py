import asyncio

from fastapi import Depends

from src.model import JevQuestions, MindcaseJob, PostModel, ScarapperModel
from src.service.jev.jevService import JevService
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
        questionsTask = asyncio.create_task(self.openAiService.generateJevQuestions(request.prompt))
        sources = await self.openAiService.generateSources(request.prompt)
        jobs = self.mindcaseService.buildJobs(sources)
        result = await self.processJobs(jobs, questionsTask)
        return {"sources": {platform.name: targets for platform, targets in sources.items()}, **result}

    async def processJobs(self, jobs: list[MindcaseJob], questionsTask: "asyncio.Task[JevQuestions]"):
        scrapeTasks = {asyncio.create_task(self.mindcaseService.runJob(job)): job for job in jobs}
        questions = await questionsTask

        seenPostIds: set[tuple[str, str]] = set()
        validPosts: list[PostModel] = []
        failed: dict[str, str] = {}
        async for task in asyncio.as_completed(scrapeTasks):
            job = scrapeTasks[task]
            if task.exception():
                failed[f"{job.platform.name}:{job.target}"] = str(task.exception())
                continue
            
            newPosts: list[PostModel] = []
            # checked one by one so a post repeated inside the same job is also dropped
            for post in task.result():
                key = (job.platform.name, post.postId)
                if key not in seenPostIds:
                    seenPostIds.add(key)
                    newPosts.append(post)
            validPosts.extend(await self.jevService.extractPostData(newPosts, questions))

        return {
            "questions": list(questions.keys()),
            "posts": len(seenPostIds),
            "validPosts": validPosts,
            "failed": failed,
        }
