from pydantic import BaseModel

class GenerateInstructions(BaseModel):
    topics: list[str]
    pass