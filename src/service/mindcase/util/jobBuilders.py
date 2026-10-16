from src.config import MINDCASE_BASE_URL
from src.model import MindcaseJob
from src.service.mindcase.enum.socialWebEnum import SocialWebEnum

POSTS_NEWER_THAN = "2026-01-01"
MAX_RESULTS = 60


def facebookJob(page: str) -> MindcaseJob:
    return MindcaseJob(
        platform=SocialWebEnum.FaceBook,
        target=page,
        url=f"{MINDCASE_BASE_URL}{SocialWebEnum.FaceBook.value}",
        params={"urls": f"https://www.facebook.com/{page}", "maxResults": MAX_RESULTS, "onlyPostsNewerThan": POSTS_NEWER_THAN, "onlyPostsOlderThan": ""},
    )


def instagramJob(handle: str) -> MindcaseJob:
    return MindcaseJob(
        platform=SocialWebEnum.Instagram,
        target=handle,
        url=f"{MINDCASE_BASE_URL}{SocialWebEnum.Instagram.value}",
        params={"handles": handle, "tab": "posts", "maxResults": MAX_RESULTS, "onlyPostsNewerThan": POSTS_NEWER_THAN},
    )


def tiktokJob(profile: str) -> MindcaseJob:
    return MindcaseJob(
        platform=SocialWebEnum.TikTok,
        target=profile,
        url=f"{MINDCASE_BASE_URL}{SocialWebEnum.TikTok.value}",
        params={"profiles": profile, "resultsPerPage": MAX_RESULTS},
    )
