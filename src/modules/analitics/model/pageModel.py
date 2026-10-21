

from src.model.facebookPageModel import FacebookPageModel
from src.model.instagramPageModel import InstagramPageModel
from src.model.tiktokPageModel import TikTokPageModel
from src.modules.analitics.model.socialWebEnum import SocialWebEnum


PageModel = FacebookPageModel | InstagramPageModel | TikTokPageModel

pageModels: dict[SocialWebEnum, type[PageModel]] = {
    SocialWebEnum.FaceBook: FacebookPageModel,
    SocialWebEnum.Instagram: InstagramPageModel,
    SocialWebEnum.TikTok: TikTokPageModel,
}
