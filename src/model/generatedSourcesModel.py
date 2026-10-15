from pydantic import BaseModel, Field

from src.service.mindcase.enum.socialWebEnum import SocialWebEnum


class GeneratedSources(BaseModel):
    FaceBook: list[str] = Field(description="Facebook page names as in the page url, e.g. 'nike'")
    Instagram: list[str] = Field(description="Instagram handles without @, e.g. 'natgeo'")
    TikTok: list[str] = Field(description="TikTok profile names without @, e.g. 'khaby.lame'")

    def toSources(self) -> dict[SocialWebEnum, list[str]]:
        return {SocialWebEnum[name]: targets for name, targets in self.model_dump().items() if targets}
