from fastapi import Depends

from src.modules.analitics.analiticsService import AnaliticsServiceClass
from src.modules.analitics.model.anliticsModel import AnaliticsModel
from src.modules.analitics.model.generateInstructions import GenerateInstructions
from src.model.openAi.generateInstructions import GeneratedInstructions


class AnaliticsController():
    analiticsService: AnaliticsServiceClass

    def __init__(self, analiticsService: AnaliticsServiceClass = Depends(AnaliticsServiceClass)):
        self.analiticsService = analiticsService

    async def generateInstructions(self, request: GenerateInstructions) -> GeneratedInstructions:
        return await self.analiticsService.generateInstructions(request)

    async def analyzePosts(self, request: AnaliticsModel):
        return await self.analiticsService.analyzePosts(request)
