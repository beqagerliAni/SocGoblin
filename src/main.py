from fastapi import FastAPI
from contextlib import asynccontextmanager

from src import config
from src.router.appRouter import router
from src.service.opensearch.opensearch import OpenSearch

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("webGoblin is Starting")
    for name in ("MINDCASE_KEY", "MINDCASE_BASE_URL", "JEV_KEY", "OPENAI_KEY"):
        if not getattr(config, name):
            print(f"warning: {name} is missing in src/.env")
    openSearch = OpenSearch()
    try:
        await openSearch.createIndexes()
    except Exception as error:
        print(f"warning: opensearch indexes were not created: {error}")
    finally:
        await openSearch.close()
    yield
    print("webGoblin has been shut down")


app = FastAPI(lifespan=lifespan)
app.include_router(router)
