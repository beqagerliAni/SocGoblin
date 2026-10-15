from dataclasses import dataclass
from typing import Any

from src.service.mindcase.enum.socialWebEnum import SocialWebEnum


# everything needed to run one mindcase scrape
@dataclass(frozen=True)
class MindcaseJob:
    platform: SocialWebEnum
    target: str  # the link or name the job was built from
    url: str
    params: dict[str, Any]
