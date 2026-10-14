from openai import AsyncOpenAI
from typesafe_sdk import Choice, Noul, Score

from src.config import OPENAI_KEY
from src.model import ChoiceQuestion, GeneratedQuestions, JevQuestions, NoulQuestion
from src.service.openai.prompts.prompts import SYSTEM_PROMPT


class OpenAiService():
    def __init__(self, model: str = "gpt-6-luna"):
        self.model = model

    async def generateQuestions(self, prompt: str) -> GeneratedQuestions:
        async with AsyncOpenAI(api_key=OPENAI_KEY) as client:
            response = await client.responses.parse(
                model=self.model,
                instructions=SYSTEM_PROMPT,
                input=prompt,
                text_format=GeneratedQuestions,
            )
        return response.output_parsed

    async def generateJevQuestions(self, prompt: str) -> JevQuestions:
        generated = await self.generateQuestions(prompt)
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
