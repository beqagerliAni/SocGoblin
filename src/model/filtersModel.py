from pydantic import BaseModel, Field


class FiltersModel(BaseModel):
    ContentInformation: str = Field(description="One sentence describing what a matching post is about")
    hashtags: list[str] = Field(description="Hashtags a matching post would use, with #, e.g. '#usedcars'")
