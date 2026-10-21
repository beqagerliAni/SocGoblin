from fastapi import Depends

from src.modules.analitics.analiticsService import AnaliticsServiceClass
from src.modules.analitics.model.commentComplaints import CommentComplaintsModel
from src.modules.analitics.model.generateInstructions import GenerateInstructions
from src.modules.analitics.model.postTopicModel import PostTopicModel
from src.model.openAi.generateInstructions import GeneratedInstructions


class AnaliticsController():
    analiticsService: AnaliticsServiceClass

    def __init__(self, analiticsService: AnaliticsServiceClass = Depends(AnaliticsServiceClass)):
        self.analiticsService = analiticsService

    async def generateInstructions(self, request: GenerateInstructions) -> GeneratedInstructions:
        return await self.analiticsService.generateInstructions(request)

    async def analyzePosts(self, request: list[PostTopicModel]):
        return await self.analiticsService.analyzePosts(request)

    async def analyzeComments(self, request: list[CommentComplaintsModel]):
        return await self.analiticsService.analyzeComments(request)
