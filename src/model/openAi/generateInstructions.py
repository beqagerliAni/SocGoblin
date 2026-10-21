from pydantic import BaseModel


class GeneratedInstructions(BaseModel):
    instructions: str
