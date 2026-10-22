from fastapi import APIRouter, Depends
from src.modules.analitics.model.commentComplaints import CommentComplaintsModel
from src.modules.analitics.model.generateInstructions import GenerateInstructions
from src.modules.analitics.model.postTopicModel import PostTopicModel
from src.model.openAi.generateInstructions import GeneratedInstructions
from src.modules.analitics.analiticsController import AnaliticsController

router = APIRouter(prefix="/analitics", tags=["analitics"])


@router.post("/instructions")
async def generateInstructions(request: GenerateInstructions, analiticsController: AnaliticsController = Depends(AnaliticsController)) -> GeneratedInstructions:
    return await analiticsController.generateInstructions(request)


@router.post("/analyze/posts")
async def analyzePosts(request: list[PostTopicModel], analiticsController: AnaliticsController = Depends(AnaliticsController)):
    return await analiticsController.analyzePosts(request)


@router.post("/analyze/comments")
async def analyzeComments(request: list[CommentComplaintsModel], analiticsController: AnaliticsController = Depends(AnaliticsController)):
    return await analiticsController.analyzeComments(request)
