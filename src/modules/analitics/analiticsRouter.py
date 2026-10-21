from fastapi import APIRouter, Depends
from src.modules.analitics.model.anliticsModel import AnaliticsModel
from src.modules.analitics.model.generateInstructions import GenerateInstructions
from src.model.openAi.generateInstructions import GeneratedInstructions
from src.modules.analitics.analiticsController import AnaliticsController

router = APIRouter(prefix="/analitics", tags=["analitics"])


@router.post("/instructions")
async def generateInstructions(request: GenerateInstructions, analiticsController: AnaliticsController = Depends(AnaliticsController)) -> GeneratedInstructions:
    return await analiticsController.generateInstructions(request)


@router.post("/analyze")
async def analyzePosts(request: AnaliticsModel, analiticsController: AnaliticsController = Depends(AnaliticsController)):
    return await analiticsController.analyzePosts(request)
