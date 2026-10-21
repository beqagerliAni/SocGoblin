from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class FacebookCommentModel(BaseModel):
    postUrl: str
    postId: str
    pageId: Optional[str] = None
    commentUrl: str
    commentText: Optional[str] = None
    commentDate: Optional[datetime] = None
    likes: int = 0
    replies: int = 0
    replyDepth: int = 0
    isReply: bool = False
    commenter: Optional[str] = None
    commenterUrl: Optional[str] = None
    commenterId: Optional[str] = None
    commenterPicture: Optional[str] = None
    replyingTo: Optional[Any] = None
    replyingToDetails: Optional[Any] = None
    threadRootAuthor: Optional[str] = None
    commentMediaType: Optional[str] = None
    commentMediaCaption: Optional[str] = None
    commentMediaUrl: Optional[str] = None
    postCaption: Optional[str] = None
