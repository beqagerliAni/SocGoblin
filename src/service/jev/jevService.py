import asyncio
from typing import Optional

from typesafe_sdk import AsyncTypeSafeClient
from src.config import JEV_KEY
from src.model import JevQuestions, PageModel

class JevService:
    def __init__(self, maxParallel: int = 10):
        self.maxParallel = maxParallel

    async def extractPostData(self, state:list[PageModel], questions:JevQuestions, threshold: float = 0.5) -> list[PageModel]:
        limit = asyncio.Semaphore(self.maxParallel)
        async with AsyncTypeSafeClient(api_key=JEV_KEY, model="jev-latest") as client:
            # all posts are checked at the same time, gather keeps their order
            results = await asyncio.gather(
                *(self.checkPost(client, limit, post, questions, threshold) for post in state)
            )
        return [post for post in results if post is not None]

    async def checkPost(self, client: AsyncTypeSafeClient, limit: asyncio.Semaphore, post: PageModel, questions: JevQuestions, threshold: float) -> Optional[PageModel]:
        text = (post.text or "").strip()
        if not text:
            return None
        async with limit:
            response = await client.system_one(text, questions)
        nouls = [answer for answer in response.answers.values() if answer.type == "noul"]
        if all(answer.noul >= threshold for answer in nouls):
            return post
        return None
