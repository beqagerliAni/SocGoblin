from datetime import datetime
from typing import Optional

from pydantic import BaseModel, computed_field


class InstagramPageComment(BaseModel):
    text: Optional[str] = None
    likes: int = 0
    authorId: Optional[str] = None
    username: Optional[str] = None
    timestamp: Optional[datetime] = None


class InstagramPageModel(BaseModel):
    postUrl: str
    caption: Optional[str] = None
    type: Optional[str] = None
    contentFormat: Optional[str] = None
    posted: datetime
    source: Optional[str] = None
    authorUsername: str
    authorName: Optional[str] = None
    authorProfileUrl: Optional[str] = None
    authorVerified: Optional[bool] = None
    authorId: Optional[str] = None
    likes: Optional[int] = None
    likesHidden: bool = False
    comments: Optional[int] = None
    plays: Optional[int] = None
    views: Optional[int] = None
    shares: Optional[int] = None
    image: Optional[str] = None
    videoUrl: Optional[str] = None
    carouselImages: list[str] = []
    carouselSlideMediaUrls: list[str] = []
    durationS: Optional[float] = None
    hashtags: list[str] = []
    mentions: list[str] = []
    firstComment: Optional[str] = None
    latestComments: list[InstagramPageComment] = []
    captionLanguage: Optional[str] = None
    locationName: Optional[str] = None
    paidPartnership: bool = False
    pinned: Optional[bool] = None
    song: Optional[str] = None
    artist: Optional[str] = None
    originalAudio: Optional[bool] = None
    taggedUsers: list[str] = []
    coauthors: list[str] = []

    # mindcase sends no id, the shortcode in the url is unique per post
    @computed_field
    @property
    def postId(self) -> str:
        return self.postUrl.rstrip("/").rsplit("/", 1)[-1]

    # jev reads the post text from here
    @property
    def text(self) -> Optional[str]:
        return self.caption
