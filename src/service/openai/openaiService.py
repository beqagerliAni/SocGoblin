from openai import AsyncOpenAI
from pydantic import BaseModel
from typesafe_sdk import Choice, Noul, Score

from src.config import OPENAI_KEY
from src.model import ChoiceQuestion, GeneratedQuestions, GeneratedSources, JevQuestions, NoulQuestion
from src.service.mindcase.enum.socialWebEnum import SocialWebEnum
from src.service.openai.prompts.prompts import SOURCES_PROMPT, SYSTEM_PROMPT


class OpenAiService():
    def __init__(self, model: str = "gpt-6-luna"):
        self.model = model

    async def structuredOutput[T: BaseModel](self, prompt: str, structure: type[T], instructions: str | None = None) -> T:
        async with AsyncOpenAI(api_key=OPENAI_KEY) as client:
            response = await client.responses.parse(
                model=self.model,
                instructions=instructions,
                input=prompt,
                text_format=structure,
            )
        return response.output_parsed

    async def generateSources(self, prompt: str) -> dict[SocialWebEnum, list[str]]:
        generated = await self.structuredOutput(prompt, GeneratedSources, SOURCES_PROMPT)
        return generated.toSources()

    async def generateJevQuestions(self, prompt: str) -> JevQuestions:
        generated = await self.structuredOutput(prompt, GeneratedQuestions, SYSTEM_PROMPT)
        questions: JevQuestions = {}
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
