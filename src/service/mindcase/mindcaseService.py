import asyncio

import httpx

from src.config import MINDCASE_BASE_URL, MINDCASE_KEY
from src.model import FacebookPostModel


class MindcaseService():
    def __init__(self):
        self.apiKey = MINDCASE_KEY
        self.baseUrl = MINDCASE_BASE_URL

    async def parseFacebookGroup(self, links: list[str], maxResults: int = 10) -> list[FacebookPostModel]:
        posts: dict[str, FacebookPostModel] = {}
        # skip groups sent more than once, scrape the rest at the same time
        uniqueLinks = dict.fromkeys(link.strip() for link in links)
        groups = await asyncio.gather(*(self.parseSingleFacebookGroup(link, maxResults) for link in uniqueLinks))
        # same post can show up twice, keep one per postId
        for groupPosts in groups:
            for post in groupPosts:
                posts.setdefault(post.postId, post)
        return list(posts.values())

    async def parseSingleFacebookGroup(self, link: str, maxResults: int = 10) -> list[FacebookPostModel]:
        async with httpx.AsyncClient(timeout=300) as client:
            resp = await client.post(
                f"{self.baseUrl}/data/facebook/posts/run",
                params={"wait": "true"},
                headers={"Authorization": f"Bearer {self.apiKey}"},
                json={"params": {
                    "groupUrls": link,
                    "maxResults": maxResults,
                }},
            )
        resp.raise_for_status()
        body = resp.json()
        # mindcase answers 200 even when the job failed, the reason is in "error"
        if body.get("status") == "failed" or "data" not in body:
            raise RuntimeError(body.get("error") or f"mindcase job did not return data for {link}")
        rows = body["data"]
        return [FacebookPostModel(**row) for row in rows]
    