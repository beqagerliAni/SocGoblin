from typing import Any

from src.service.mindcase.enum.socialWebEnum import SocialWebEnum
from src.service.opensearch.mapping.facebookMapping import facebookMapping
from src.service.opensearch.mapping.instagramMapping import instagramMapping
from src.service.opensearch.mapping.tiktokMapping import tiktokMapping

indexes: dict[SocialWebEnum, dict[str, Any]] = {
    SocialWebEnum.FaceBook: {"name": "webgoblin-facebook", "mapping": facebookMapping, "dateField": "postedAt", "nameField": "source.name"},
    SocialWebEnum.Instagram: {"name": "webgoblin-instagram", "mapping": instagramMapping, "dateField": "posted", "nameField": "authorUsername"},
    SocialWebEnum.TikTok: {"name": "webgoblin-tiktok", "mapping": tiktokMapping, "dateField": "postedDate", "nameField": "sourceQuery"},
}
