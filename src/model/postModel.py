from src.service.mindcase.enum.socialWebEnum import SocialWebEnum

from .facebookPostModel import FacebookPostModel
from .instagramPostModel import InstagramPostModel
from .tiktokPostModel import TikTokPostModel

PostModel = FacebookPostModel | InstagramPostModel | TikTokPostModel

# which model a mindcase row turns into, per platform
postModels: dict[SocialWebEnum, type[PostModel]] = {
    SocialWebEnum.FaceBook: FacebookPostModel,
    SocialWebEnum.Instagram: InstagramPostModel,
    SocialWebEnum.TikTok: TikTokPostModel,
}
