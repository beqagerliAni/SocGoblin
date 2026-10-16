import asyncio
from typing import Optional

from typesafe_sdk import AsyncTypeSafeClient, Noul
from src.config import JEV_KEY
from src.model import FiltersModel, JevQuestions, PageModel
from src.service.jev.util.stateBuilder import buildState

class JevService:
    
    def __init__(self, maxParallel: int = 20):
        self.client = AsyncTypeSafeClient(api_key=JEV_KEY, model="jev-latest")
        self.maxParallel = maxParallel

    def buildNoulQuestions(self, filters: FiltersModel, instructions: str) -> JevQuestions:
        questions: JevQuestions = {
            "content_information": Noul(
                instructions=instructions,
                criteria={
                    "true": f"The post is about: {filters.ContentInformation}",
                    "false": f"The post is not about: {filters.ContentInformation}",
                },
            ),
        }
        return questions

    async def extractPostData(self, state:list[PageModel], questions:JevQuestions, threshold: float = 0.6) -> tuple[list[PageModel], dict[str, str]]:
        limit = asyncio.Semaphore(self.maxParallel)
        failedPosts: dict[str, str] = {}
        results = await asyncio.gather(
            *(self.checkPost(limit, post, questions, threshold, failedPosts) for post in state)
        )
        return [post for post in results if post is not None], failedPosts

    async def checkPost(self, limit: asyncio.Semaphore, post: PageModel, questions: JevQuestions, threshold: float, failedPosts: dict[str, str]) -> Optional[PageModel]:
        state = buildState(post, ["text"])
        if state is None:
            print(f"[jev] skip {post.postUrl}: no text")
            return None
        try:
            async with limit:
                response = await self.client.system_one(state, questions)
        except Exception as error:
            failedPosts[post.postUrl] = str(error) or type(error).__name__
            print(f"[jev] ERROR {post.postUrl}: {failedPosts[post.postUrl]}")
            return None
        nouls = [answer for answer in response.answers.values() if answer.type == "noul"]
        print(f"[jev] {post.postUrl} " + ", ".join(f"{name}={answer.noul:.2f}" for name, answer in response.answers.items() if answer.type == "noul"))
        if all(answer.noul >= threshold for answer in nouls):
            return post
        return None
