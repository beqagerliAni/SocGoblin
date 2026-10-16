from datetime import date

from opensearchpy import AsyncOpenSearch
from opensearchpy.helpers import async_bulk, async_scan

from src.config import OPENSEARCH_PASSWORD, OPENSEARCH_URL, OPENSEARCH_USER, OPENSEARCH_VERIFY_CERTS
from src.model import PageModel, pageModels
from src.service.mindcase.enum.socialWebEnum import SocialWebEnum
from src.service.opensearch.types.indexTypes import indexes


class OpenSearch():
    def __init__(self):
        auth = (OPENSEARCH_USER, OPENSEARCH_PASSWORD) if OPENSEARCH_USER else None
        self.client = AsyncOpenSearch(
            hosts=[OPENSEARCH_URL],
            http_auth=auth,
            verify_certs=OPENSEARCH_VERIFY_CERTS,
            ssl_show_warn=OPENSEARCH_VERIFY_CERTS,
        )

    async def close(self):
        await self.client.close()

    async def createIndexes(self):
        for index in indexes.values():
            if not await self.client.indices.exists(index=index["name"]):
                await self.client.indices.create(index=index["name"], body=index["mapping"])

    async def getDocuments(self, since: date, name: str, platform: SocialWebEnum | None = None) -> list[PageModel]:
        documents: list[PageModel] = []
        for indexPlatform, index in indexes.items():
            if platform and indexPlatform != platform:
                continue
            if not await self.client.indices.exists(index=index["name"]):
                continue
            query = {"query": {"bool": {"filter": [
                {"range": {index["dateField"]: {"gte": since.isoformat()}}},
                {"term": {index["nameField"]: {"value": name, "case_insensitive": True}}},
            ]}}}
            async for hit in async_scan(self.client, index=index["name"], query=query):
                documents.append(pageModels[indexPlatform](**hit["_source"]))
        return documents

    async def bulkUpload(self, platform: SocialWebEnum, posts: list[PageModel]) -> int:
        index = indexes[platform]
        if not await self.client.indices.exists(index=index["name"]):
            await self.client.indices.create(index=index["name"], body=index["mapping"])
        actions = (
            {"_index": index["name"], "_id": post.postId, "_source": post.model_dump(mode="json")}
            for post in posts
        )
        uploaded, _ = await async_bulk(self.client, actions)
        return uploaded
