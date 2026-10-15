import httpx

from src.config import MINDCASE_KEY
from src.model import MindcaseJob, PostModel, postModels
from src.service.mindcase.enum.socialWebEnum import SocialWebEnum
from src.service.mindcase.types.jobBuilderTypes import jobBuilders


class MindcaseService():
    def __init__(self):
        self.apiKey = MINDCASE_KEY

    def buildJobs(self, sources: dict[SocialWebEnum, list[str]]) -> list[MindcaseJob]:
        jobs: list[MindcaseJob] = []
        for platform, targets in sources.items():
            for target in dict.fromkeys(target.strip() for target in targets):
                jobs.append(jobBuilders[platform](target))
        return jobs

    async def runJob(self, job: MindcaseJob) -> list[PostModel]:
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
        model = postModels[job.platform]
        return [model(**row) for row in body["data"]]
