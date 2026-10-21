import json
from pathlib import Path

from src.model import FacebookPageModel
from src.modules.analitics.model.facebookCommentModel import FacebookCommentModel

DATA_PATH = Path(__file__).parents[3] / "data" / "data.json"
COMMENTS_DATA_PATH = Path(__file__).parents[3] / "data" / "commentsData.json"


def loadDummyPosts() -> list[FacebookPageModel]:
    return [FacebookPageModel.model_validate(post) for post in json.loads(DATA_PATH.read_text())]


def loadDummyComments() -> list[FacebookCommentModel]:
    return [FacebookCommentModel.model_validate(comment) for comment in json.loads(COMMENTS_DATA_PATH.read_text())]
