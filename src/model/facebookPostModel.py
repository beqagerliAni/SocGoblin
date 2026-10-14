from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class FacebookPostAuthor(BaseModel):
    id: str
    url: Optional[str] = None
    name: str
    avatar: Optional[str] = None


class FacebookPostComment(BaseModel):
    url: Optional[str] = None
    date: Optional[datetime] = None
    text: Optional[str] = None
    likes: int = 0
    author: Optional[str] = None


class FacebookPostSource(BaseModel):
    url: str
    name: str


class FacebookPostMedia(BaseModel):
    url: Optional[str] = None
    type: Optional[str] = None
    imageOcr: Optional[str] = None
    videoUrl: Optional[str] = None
    thumbnailUrl: Optional[str] = None


class FacebookPostModel(BaseModel):
    contentType: str
    postUrl: str
    postId: str
    postedAt: datetime
    text: Optional[str] = None
    reactions: int = 0
    comments: int = 0
    shares: int = 0
    views: Optional[int] = None
    videoDuration: Optional[float] = None
    reactionBreakdown: Optional[dict[str, Optional[int]]] = None
    author: FacebookPostAuthor
    source: Optional[FacebookPostSource] = None
    media: Optional[FacebookPostMedia] = None
    linkPreview: Optional[dict[str, Any]] = None
    mentions: list[Any] = []
    collaborators: list[Any] = []
    topComments: list[FacebookPostComment] = []
    hashtags: Optional[list[str]] = None
