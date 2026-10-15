from fastapi import APIRouter, Depends

from src.model import ScarapperModel
from src.service.app.appService import AppService

router = APIRouter(prefix="/socicalGoblin", tags=["socialGoblin"])


@router.post("/scrape")
async def scrapeGroups(request: ScarapperModel, appService: AppService = Depends(AppService)):
    return await appService.scrapeGroups(request)
