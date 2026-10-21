from typing import Any

from src.modules.analitics.model.facebookCommentModel import FacebookCommentModel
from src.service.jev.util.stateBuilder import buildState


def buildCommentStates(comments: list[FacebookCommentModel]) -> dict[str, dict[str, Any]]:
    return {comment.commentUrl: state for comment in comments if (state := buildState(comment, ["commentText"])) is not None}
