from src.config import MINDCASE_BASE_URL
from src.model import MindcaseJob
from src.service.mindcase.enum.socialWebEnum import SocialWebEnum


def facebookJob(page: str, maxResults: int = 10) -> MindcaseJob:
    return MindcaseJob(
        platform=SocialWebEnum.FaceBook,
        target=page,
        url=f"{MINDCASE_BASE_URL}{SocialWebEnum.FaceBook.value}",
        params={"urls": f"https://www.facebook.com/{page}", "maxResults": maxResults, "onlyPostsNewerThan": "", "onlyPostsOlderThan": ""},
    )


def instagramJob(handle: str) -> MindcaseJob:
    return MindcaseJob(
        platform=SocialWebEnum.Instagram,
        target=handle,
        url=f"{MINDCASE_BASE_URL}{SocialWebEnum.Instagram.value}",
        params={"handles": handle, "tab": "posts", "onlyPostsNewerThan": ""},
    )


def tiktokJob(profile: str) -> MindcaseJob:
    return MindcaseJob(
        platform=SocialWebEnum.TikTok,
        target=profile,
        url=f"{MINDCASE_BASE_URL}{SocialWebEnum.TikTok.value}",
        params={"profiles": profile},
    )
