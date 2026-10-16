from typing import Any, Optional

from src.model import PageModel


def buildState(post: PageModel, fields: list[str]) -> Optional[dict[str, Any]]:
    state: dict[str, Any] = {}
    for field in fields:
        value = getattr(post, field, None)
        if isinstance(value, str):
            value = value.strip()
        state[field] = value
    if not any(state.values()):
        return None
    return state
