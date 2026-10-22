from pydantic import BaseModel


class JevDataModel(BaseModel):
    id: str
    text: str


class BaseJevQuestionModel(BaseModel):
    analiticName: str
    topics: list[str]
    instructions: str
    data: list[JevDataModel]
