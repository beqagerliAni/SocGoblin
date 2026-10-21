import asyncio
from typing import Any, Optional

from typesafe_sdk import AsyncTypeSafeClient, Choice, ChoiceAnswer
from src.config import JEV_KEY
from src.modules.analitics.model.shared.baseJevQuestionModel import BaseJevQuestionModel

class JevService:
    
    def __init__(self, maxParallel: int = 20):
        self.client = AsyncTypeSafeClient(api_key=JEV_KEY, model="jev-latest")
        self.maxParallel = maxParallel

    def buildChoiceQuestions(self, questions: list[BaseJevQuestionModel]) -> dict[str, Choice]:
        return {
            question.analiticName: Choice(instructions=question.instructions, criteria={topic: None for topic in question.topics})
            for question in questions
        }

    async def chooseTopics(self, states: dict[str, dict[str, Any]], questions: dict[str, Choice]) -> tuple[dict[str, dict[str, ChoiceAnswer]], dict[str, str]]:
        limit = asyncio.Semaphore(self.maxParallel)
        failed: dict[str, str] = {}
        results = await asyncio.gather(
            *(self.chooseTopic(limit, key, state, questions, failed) for key, state in states.items())
        )
        return {key: answers for key, answers in results if answers is not None}, failed

    async def chooseTopic(self, limit: asyncio.Semaphore, key: str, state: dict[str, Any], questions: dict[str, Choice], failed: dict[str, str]) -> tuple[str, Optional[dict[str, ChoiceAnswer]]]:
        try:
            async with limit:
                response = await self.client.system_one(state, questions)
        except Exception as error:
            failed[key] = str(error) or type(error).__name__
            return key, None
        return key, response.choices
