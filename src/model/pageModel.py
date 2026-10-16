from src.service.mindcase.enum.socialWebEnum import SocialWebEnum

from .facebookPageModel import FacebookPageModel
from .instagramPageModel import InstagramPageModel
from .tiktokPageModel import TikTokPageModel

PageModel = FacebookPageModel | InstagramPageModel | TikTokPageModel

pageModels: dict[SocialWebEnum, type[PageModel]] = {
    SocialWebEnum.FaceBook: FacebookPageModel,
    SocialWebEnum.Instagram: InstagramPageModel,
    SocialWebEnum.TikTok: TikTokPageModel,
}
