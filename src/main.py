from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("webGoblin is Starting")
    yield
    print("webGoblin has been shut down")


app = FastAPI(lifespan=lifespan)

@app.get("/items/webScrapper")
async def scrapePerson(scrapperModel):
    #we will get hear scrapperModel.personName
    # split it and after that get firstName and lastName
    pass
