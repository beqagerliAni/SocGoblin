from pydantic import BaseModel

class BaseJevQuestionModel(BaseModel):
    analiticName: str
    topics: list[str]
    instructions: str
