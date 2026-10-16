from datetime import date, datetime, timezone

import httpx
from pydantic import ValidationError

from src.config import MINDCASE_KEY
from src.model import MindcaseJob, PageModel, pageModels
from src.service.mindcase.enum.socialWebEnum import SocialWebEnum
from src.service.mindcase.types.jobBuilderTypes import jobBuilders
from src.service.mindcase.util.jobBuilders import POSTS_NEWER_THAN


class MindcaseService():
    def __init__(self):
        self.apiKey = MINDCASE_KEY

    def buildJobs(self, sources: dict[SocialWebEnum, list[str]]) -> list[MindcaseJob]:
        jobs: list[MindcaseJob] = []
        for platform, targets in sources.items():
            for target in dict.fromkeys(target.strip() for target in targets):
                jobs.append(jobBuilders[platform](target))
        return jobs

    async def runJob(self, job: MindcaseJob) -> list[PageModel]:
        async with httpx.AsyncClient(timeout=300) as client:
            resp = await client.post(
                job.url,
                params={"wait": "true"},
                headers={"Authorization": f"Bearer {self.apiKey}"},
                json={"params": job.params},
            )
        resp.raise_for_status()
        body = resp.json()
        if body.get("status") == "failed" or "data" not in body:
            raise RuntimeError(body.get("error") or f"mindcase job did not return data for {job.target}")
        model = pageModels[job.platform]
        posts: list[PageModel] = []
        for row in body["data"]:
            try:
                posts.append(model(**row))
            except ValidationError:
                continue
        since = datetime.combine(date.fromisoformat(POSTS_NEWER_THAN), datetime.min.time(), timezone.utc)
        newPosts = [post for post in posts if post.publishedAt.replace(tzinfo=post.publishedAt.tzinfo or timezone.utc) >= since]
        return newPosts
