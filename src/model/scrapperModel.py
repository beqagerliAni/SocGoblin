from pydantic import BaseModel, ConfigDict, Field


class ScarapperModel(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "examples": [{"prompt": "people looking to buy a used car"}],
    })
    prompt: str = Field(min_length=1, description="What kind of posts you are looking for")
