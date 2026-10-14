import asyncio
from typing import Optional

from typesafe_sdk import AsyncTypeSafeClient
from src.config import JEV_KEY
from src.model import FacebookPostModel
from src.model import JevQuestions

class JevService:
    def __init__(self, maxParallel: int = 10):
        # how many posts jev checks at the same time
        self.maxParallel = maxParallel

    # define state modal
    async def extractPostData(self, state:list[FacebookPostModel], questions:JevQuestions, threshold: float = 0.5) -> list[FacebookPostModel]:
        limit = asyncio.Semaphore(self.maxParallel)
        async with AsyncTypeSafeClient(api_key=JEV_KEY, model="jev-latest") as client:
            # all posts are checked at the same time, gather keeps their order
            results = await asyncio.gather(
                *(self.checkPost(client, limit, post, questions, threshold) for post in state)
            )
        return [post for post in results if post is not None]

    async def checkPost(self, client: AsyncTypeSafeClient, limit: asyncio.Semaphore, post: FacebookPostModel, questions: JevQuestions, threshold: float) -> Optional[FacebookPostModel]:
        # 1. take only the text information from the state
        text = (post.text or "").strip()
        if not text:
            return None
        # 2. ask jev the questions about the post
        async with limit:
            response = await client.system_one(text, questions)
        # 3. keep the post only if every yes/no question is answered yes
        nouls = [answer for answer in response.answers.values() if answer.type == "noul"]
        if all(answer.noul >= threshold for answer in nouls):
            return post
        return None
