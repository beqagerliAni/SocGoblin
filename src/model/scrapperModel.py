from pydantic import BaseModel, Field

class ScarapperModel(BaseModel):
    prompt: str = Field(min_length=1)
    # at least one group, so we never call openai for nothing
    grups: list[str] = Field(min_length=1)