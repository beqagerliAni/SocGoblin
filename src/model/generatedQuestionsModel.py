from typing import Literal, Optional, Union

from pydantic import BaseModel, Field
from typesafe_sdk import Choice, Noul, Score


# structured output for the questions we send to jev
class ChoiceOption(BaseModel):
    label: str = Field(description="Short snake_case label for the option, e.g. 'wants_to_buy'")
    description: str = Field(description="What this option means")


class ChoiceQuestion(BaseModel):
    type: Literal["choice"]
    key: str = Field(description="Short snake_case key for the question")
    instructions: str = Field(description="The question to ask about the post")
    options: list[ChoiceOption] = Field(description="2 to 6 mutually exclusive options")


class NoulQuestion(BaseModel):
    type: Literal["noul"]
    key: str = Field(description="Short snake_case key for the question")
    instructions: str = Field(description="A statement that is either true or false about the post")
    true: Optional[str] = Field(description="What a yes answer means, or null")
    false: Optional[str] = Field(description="What a no answer means, or null")


class ScoreQuestion(BaseModel):
    type: Literal["score"]
    key: str = Field(description="Short snake_case key for the question")
    instructions: str = Field(description="The question to rate the post on")
    levels: list[str] = Field(description="Ordered levels from lowest to highest")


class GeneratedQuestions(BaseModel):
    questions: list[Union[ChoiceQuestion, NoulQuestion, ScoreQuestion]]


JevQuestions = dict[str, Union[Choice, Noul, Score]]
