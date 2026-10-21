from pydantic import BaseModel

class BaseJevQuestionModel(BaseModel): 
    topics: list[str]
    instructions: str