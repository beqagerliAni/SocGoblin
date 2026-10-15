from typing import Callable

from src.model import MindcaseJob
from src.service.mindcase.enum.socialWebEnum import SocialWebEnum
from src.service.mindcase.util.jobBuilders import facebookJob, instagramJob, tiktokJob

jobBuilders: dict[SocialWebEnum, Callable[[str], MindcaseJob]] = {
    SocialWebEnum.FaceBook: facebookJob,
    SocialWebEnum.Instagram: instagramJob,
    SocialWebEnum.TikTok: tiktokJob,
}
