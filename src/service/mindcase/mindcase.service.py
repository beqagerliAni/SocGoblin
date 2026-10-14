import requests

from src.config import MINDCASE_BASE_URL, MINDCASE_KEY
from src.model import FacebookPostModel


class MindcaseService():
    def __init__(self):
        self.apiKey = MINDCASE_KEY
        self.baseUrl = MINDCASE_BASE_URL

    def parseFacebookGroup(self, links: list[str], maxResults: int = 100) -> list[FacebookPostModel]:
        posts: list[FacebookPostModel] = []
        for link in links:
            posts.extend(self.parseSingleFacebookGroup(link, maxResults))
        return posts

    def parseSingleFacebookGroup(self, link: str, maxResults: int = 100) -> list[FacebookPostModel]:
        resp = requests.post(
            f"{self.baseUrl}/data/facebook/posts/run",
            params={"wait": "true"},
            headers={"Authorization": f"Bearer {self.apiKey}"},
            json={"params": {
                "groupUrls": link,
                "maxResults": maxResults,
            }},
            timeout=300,
        )
        resp.raise_for_status()
        rows = resp.json()["data"]
        return [FacebookPostModel(**row) for row in rows]
