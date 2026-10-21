import asyncio
from typing import Any, Optional

from typesafe_sdk import AsyncTypeSafeClient, Choice, ChoiceAnswer
from src.config import JEV_KEY
from src.modules.analitics.model.shared.baseJevQuestionModel import BaseJevQuestionModel

class JevService:
    
    def __init__(self, maxParallel: int = 20):
        self.client = AsyncTypeSafeClient(api_key=JEV_KEY, model="jev-latest")
        self.maxParallel = maxParallel

    def buildChoiceQuestion(self, question: BaseJevQuestionModel) -> Choice:
        return Choice(instructions=question.instructions, criteria={topic: None for topic in question.topics})

    async def chooseTopics(self, states: dict[str, dict[str, Any]], question: Choice) -> tuple[dict[str, ChoiceAnswer], dict[str, str]]:
        limit = asyncio.Semaphore(self.maxParallel)
        failed: dict[str, str] = {}
        results = await asyncio.gather(
            *(self.chooseTopic(limit, key, state, question, failed) for key, state in states.items())
        )
        return {key: answer for key, answer in results if answer is not None}, failed

    async def chooseTopic(self, limit: asyncio.Semaphore, key: str, state: dict[str, Any], question: Choice, failed: dict[str, str]) -> tuple[str, Optional[ChoiceAnswer]]:
        try:
            async with limit:
                response = await self.client.system_one(state, {"topic": question})
        except Exception as error:
            failed[key] = str(error) or type(error).__name__
            print(f"[jev] ERROR {key}: {failed[key]}")
            return key, None
        answer = response.choices["topic"]
        print(f"[jev] {key} topic={answer.choice} ({answer.confidence:.2f})")
        return key, answer
