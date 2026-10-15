from datetime import datetime
from typing import Optional

from pydantic import BaseModel, computed_field


class TikTokPostAuthor(BaseModel):
    bio: Optional[str] = None
    avatar: Optional[str] = None
    videos: Optional[int] = None
    private: bool = False
    tiktokId: str
    verified: bool = False
    followers: Optional[int] = None
    following: Optional[int] = None
    likesGiven: Optional[int] = None
    profileUrl: Optional[str] = None
    totalLikes: Optional[int] = None
    displayName: Optional[str] = None
    tiktokSeller: bool = False
    mutualFollows: Optional[int] = None
    accountCreated: Optional[datetime] = None
    businessAccount: bool = False
    businessCategory: Optional[str] = None


class TikTokPostHashtag(BaseModel):
    name: str


class TikTokPostSound(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    album: Optional[str] = None
    author: Optional[str] = None
    audioUrl: Optional[str] = None
    original: Optional[bool] = None
    videoCount: Optional[int] = None


class TikTokPostModel(BaseModel):
    postUrl: str
    author: TikTokPostAuthor
    caption: Optional[str] = None
    postedDate: datetime
    views: Optional[int] = None
    likes: Optional[int] = None
    comments: Optional[int] = None
    shares: Optional[int] = None
    saves: Optional[int] = None
    language: Optional[str] = None
    isSlideshow: bool = False
    isAd: bool = False
    isSponsored: bool = False
    hashtags: list[TikTokPostHashtag] = []
    mentions: list[str] = []
    effects: list[str] = []
    slideshowImages: Optional[list[str]] = None
    photoSlideshowImageUrls: list[str] = []
    thumbnail: Optional[str] = None
    durationS: Optional[float] = None
    resolution: Optional[str] = None
    sound: Optional[TikTokPostSound] = None
    location: Optional[str] = None
    locationAddress: Optional[str] = None
    country: Optional[str] = None
    hashtagViews: Optional[int] = None
    sourceQuery: Optional[str] = None

    # mindcase sends no id, the video id is the last part of the url
    @computed_field
    @property
    def postId(self) -> str:
        return self.postUrl.rstrip("/").rsplit("/", 1)[-1]

    # jev reads the post text from here
    @property
    def text(self) -> Optional[str]:
        return self.caption
