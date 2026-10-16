from dataclasses import dataclass
from typing import Any

from src.service.mindcase.enum.socialWebEnum import SocialWebEnum


@dataclass(frozen=True)
class MindcaseJob:
    platform: SocialWebEnum
    target: str
    url: str
    params: dict[str, Any]
