from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.service.mindcase.enum.socialWebEnum import SocialWebEnum


class ScarapperModel(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "examples": [{
            "prompt": "people looking to buy a used car",
            "sources": {
                "FaceBook": ["https://www.facebook.com/groups/usedcarsforsale"],
                "Instagram": ["natgeo"],
                "TikTok": ["khaby.lame"],
            },
        }],
    })

    prompt: str = Field(min_length=1, description="What kind of posts you are looking for")
    # facebook takes group links, instagram and tiktok take handles / profile names
    sources: dict[SocialWebEnum, list[str]] = Field(
        min_length=1,
        description="Platform name to what to scrape: FaceBook takes group links, Instagram and TikTok take handles",
        # swagger shows the names people send, not the endpoint values
        json_schema_extra={"propertyNames": {"enum": list(SocialWebEnum.__members__)}},
    )

    # the request uses the platform name ("FaceBook"), the enum value is the endpoint
    @field_validator("sources", mode="before")
    @classmethod
    def platformByName(cls, sources: Any) -> Any:
        if not isinstance(sources, dict):
            return sources
        return {SocialWebEnum[key] if key in SocialWebEnum.__members__ else key: links for key, links in sources.items()}
