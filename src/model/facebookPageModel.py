from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class FacebookPageAuthor(BaseModel):
    id: str
    url: Optional[str] = None
    name: str
    avatar: Optional[str] = None


class FacebookPageComment(BaseModel):
    url: Optional[str] = None
    date: Optional[datetime] = None
    text: Optional[str] = None
    likes: int = 0
    author: Optional[str] = None


class FacebookPageSource(BaseModel):
    url: str
    name: str


class FacebookPageMedia(BaseModel):
    url: Optional[str] = None
    type: Optional[str] = None
    imageOcr: Optional[str] = None
    videoUrl: Optional[str] = None
    thumbnailUrl: Optional[str] = None


class FacebookPageModel(BaseModel):
    contentType: str
    postUrl: str
    postId: str
    postedAt: datetime
    text: Optional[str] = None
    reactions: int = 0
    comments: Optional[int] = None
    shares: int = 0
    views: Optional[int] = None
    videoDuration: Optional[float] = None
    reactionBreakdown: Optional[dict[str, Optional[int]]] = None
    author: FacebookPageAuthor
    source: Optional[FacebookPageSource] = None
    media: Optional[FacebookPageMedia] = None
    linkPreview: Optional[dict[str, Any]] = None
    mentions: list[Any] = []
    collaborators: list[Any] = []
    topComments: list[FacebookPageComment] = []
    hashtags: Optional[list[str]] = None
