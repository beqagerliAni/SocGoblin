from pydantic import BaseModel

class ScarapperModel(BaseModel):
    personName: str
    information: str