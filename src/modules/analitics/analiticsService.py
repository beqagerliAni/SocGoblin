import asyncio
from typing import Any

from fastapi import HTTPException
from typesafe_sdk import Choice, ChoiceAnswer

from src.modules.analitics.model.commentComplaints import CommentComplaintsModel
from src.modules.analitics.model.generateInstructions import GenerateInstructions
from src.modules.analitics.model.postTopicModel import PostTopicModel
from src.modules.analitics.model.shared.baseJevQuestionModel import BaseJevQuestionModel
from src.modules.analitics.prompt.instructionsPrompt import prompt as INSTRUCTIONS_PROMPT
from src.model.openAi.generateInstructions import GeneratedInstructions
from src.service.jev.jevService import JevService
from src.service.openai.openaiService import OpenAiService



class AnaliticsServiceClass():
    openAiService: OpenAiService
    jevService: JevService

    def __init__(self):
        self.openAiService = OpenAiService(model="gpt-6-luna")
        self.jevService = JevService()

    def topicResult(self, answer: ChoiceAnswer | None) -> dict[str, Any]:
        return {
            "topicType": answer.choice if answer else None,
            "confidence": answer.confidence if answer else None,
        }

    async def generateInstructions(self, request: GenerateInstructions) -> GeneratedInstructions:
        topics = "\n".join(f"- {topic}" for topic in request.topics)
        return await self.openAiService.structuredOutput(f"Topics:\n{topics}", GeneratedInstructions, INSTRUCTIONS_PROMPT)

    def validateQuestions(self, request: list[BaseJevQuestionModel]):
        names = [question.analiticName for question in request]
        duplicates = {name for name in names if names.count(name) > 1}
        if duplicates:
            raise HTTPException(status_code=400, detail=f"analiticName must be unique, duplicated: {sorted(duplicates)}")
        for question in request:
            ids = [item.id for item in question.data]
            duplicateIds = {id for id in ids if ids.count(id) > 1}
            if duplicateIds:
                raise HTTPException(status_code=400, detail=f"data id must be unique in '{question.analiticName}', duplicated: {sorted(duplicateIds)}")

    def buildStates(self, question: BaseJevQuestionModel) -> dict[str, dict[str, Any]]:
        return {item.id: {"text": text} for item in question.data if (text := item.text.strip())}

    def analiticsResult(self, questions: dict[str, Choice], answers: dict[str, ChoiceAnswer] | None) -> dict[str, dict[str, Any]]:
        return {name: self.topicResult((answers or {}).get(name)) for name in questions}

    async def analyzeQuestion(self, question: BaseJevQuestionModel) -> dict[str, Any]:
        questions = self.jevService.buildChoiceQuestions([question])
        answers, failed = await self.jevService.chooseTopics(self.buildStates(question), questions)
        return {
            "data": [
                {"id": item.id, "text": item.text, "analitics": self.analiticsResult(questions, answers.get(item.id))}
                for item in question.data
            ],
            "failed": failed,
        }

    async def analyze(self, request: list[BaseJevQuestionModel]) -> dict[str, dict[str, Any]]:
        self.validateQuestions(request)
        results = await asyncio.gather(*(self.analyzeQuestion(question) for question in request))
        return {question.analiticName: result for question, result in zip(request, results)}

    async def analyzePosts(self, request: list[PostTopicModel]):
        return await self.analyze(request)

    async def analyzeComments(self, request: list[CommentComplaintsModel]):
        return await self.analyze(request)
