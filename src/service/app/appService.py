import asyncio

from fastapi import Depends

from src.model import FacebookPostModel, ScarapperModel
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
        links = list(dict.fromkeys(link.strip() for link in request.grups))

        # openai and every group start at the same time
        questionsTask = asyncio.create_task(self.openAiService.generateJevQuestions(request.prompt))
        scrapeTasks = {
            asyncio.create_task(self.mindcaseService.parseSingleFacebookGroup(link)): link
            for link in links
        }
        questions = await questionsTask

        seenPostIds: set[str] = set()
        validPosts: list[FacebookPostModel] = []
        failedGroups: dict[str, str] = {}
        # groups come in the order they finish, the ones done while jev is busy wait their turn
        async for task in asyncio.as_completed(scrapeTasks):
            if task.exception():
                # one bad group should not lose the posts of the others
                failedGroups[scrapeTasks[task]] = str(task.exception())
                continue
            newPosts = [post for post in task.result() if post.postId not in seenPostIds]
            seenPostIds.update(post.postId for post in newPosts)
            validPosts.extend(await self.jevService.extractPostData(newPosts, questions))

        return {
            "questions": list(questions.keys()),
            "posts": len(seenPostIds),
            "validPosts": validPosts,
            "failedGroups": failedGroups,
        }
