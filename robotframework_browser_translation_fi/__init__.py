from pathlib import Path
from typing import TypedDict


class Language(TypedDict):
    language: str
    path: str


def get_language() -> Language:
    folder = Path(__file__).parent

    return {"language": "fi", "path": str(folder / "translation.json")}
