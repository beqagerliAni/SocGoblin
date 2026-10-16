from pydantic import BaseModel, Field

from src.service.mindcase.enum.socialWebEnum import SocialWebEnum

from .filtersModel import FiltersModel


class GeneratedSources(BaseModel):
    FaceBook: list[str] = Field(description="Facebook page names as in the page url, e.g. 'nike'")
    Instagram: list[str] = Field(description="Instagram handles without @, e.g. 'natgeo'")
    TikTok: list[str] = Field(description="TikTok profile names without @, e.g. 'khaby.lame'")
    filters: FiltersModel

    def toSources(self) -> dict[SocialWebEnum, list[str]]:
        return {platform: getattr(self, platform.name) for platform in SocialWebEnum if getattr(self, platform.name)}
