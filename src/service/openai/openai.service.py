from typing import Union

from openai import OpenAI
from typesafe_sdk import Choice, Noul, Score

from src.config import OPENAI_KEY
from src.model import ChoiceQuestion, GeneratedQuestions, NoulQuestion
from src.service.openai.prompts.prompts import SYSTEM_PROMPT


class OpenAiService():
    client: OpenAI

    def __init__(self, model: str = "gpt-5.5"):
        self.client = OpenAI(api_key=OPENAI_KEY)
        self.model = model

    def generateQuestions(self, prompt: str) -> GeneratedQuestions:
        response = self.client.responses.parse(
            model=self.model,
            instructions=SYSTEM_PROMPT,
            input=prompt,
            text_format=GeneratedQuestions,
        )
        return response.output_parsed

    def generateJevQuestions(self, prompt: str) -> dict[str, Union[Choice, Noul, Score]]:
        generated = self.generateQuestions(prompt)
        questions: dict[str, Union[Choice, Noul, Score]] = {}
        for question in generated.questions:
            if isinstance(question, ChoiceQuestion):
                questions[question.key] = Choice(
                    instructions=question.instructions,
                    criteria={option.label: option.description for option in question.options},
                )
            elif isinstance(question, NoulQuestion):
                questions[question.key] = Noul(
                    instructions=question.instructions,
                    criteria={"true": question.true, "false": question.false},
                )
            else:
                questions[question.key] = Score(
                    instructions=question.instructions,
                    criteria=question.levels,
                )
        return questions
