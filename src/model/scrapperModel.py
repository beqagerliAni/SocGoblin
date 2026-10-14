from pydantic import BaseModel

class ScarapperModel(BaseModel):
    prompt: str
    grups: list[str]