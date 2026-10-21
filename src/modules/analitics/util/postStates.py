from enum import Enum
from typing import Any

from src.modules.analitics.model.pageModel import PageModel
from src.service.jev.util.stateBuilder import buildState


def buildPostStates(posts: list[PageModel]) -> dict[str, dict[str, Any]]:
    return {post.postUrl: state for post in posts if (state := buildState(post, ["text"])) is not None}



class SocialWebEnum(str, Enum):
    TikTok = "/data/tiktok/posts/run"
    FaceBook = "/data/facebook/posts/run"
    Instagram = "/data/instagram/posts/run"
