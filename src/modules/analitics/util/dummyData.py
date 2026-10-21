import json
from pathlib import Path

from src.model import FacebookPageModel

DATA_PATH = Path(__file__).parents[3] / "data" / "data.json"


def loadDummyPosts() -> list[FacebookPageModel]:
    return [FacebookPageModel.model_validate(post) for post in json.loads(DATA_PATH.read_text())]
