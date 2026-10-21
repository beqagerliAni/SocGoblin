from fastapi import FastAPI
from contextlib import asynccontextmanager

from src import config
from src.modules.analitics.analiticsRouter import router as analiticsRouter

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("webGoblin is Starting")
    for name in ( "JEV_KEY", "OPENAI_KEY"):
        if not getattr(config, name):
            print(f"warning: {name} is missing in src/.env")
    yield
    print("webGoblin has been shut down")


app = FastAPI(lifespan=lifespan)
app.include_router(analiticsRouter)
