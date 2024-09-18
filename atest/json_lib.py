import json
from pathlib import Path

from robot.api import logger


def compare_translations(file: Path):
    with Path(__file__).parent.parent.joinpath(
        "robotframework_browser_translation", "translation_fi.json"
    ).open("r") as file_object:
        expected_data = json.load(file_object)
    expected_keywords = [kw["name"] for kw in expected_data.values()]
    logger.info(f"expected_keywords: {expected_keywords}")
    with file.open("r") as file_object:
        data = json.load(file_object)
    keywords = data["keywords"]
    for keyword in keywords:
        logger.info(keyword)
        name = keyword["name"]
        name = name.replace(" ", "_").lower()
        assert name in expected_keywords, f"name '{name}' not in {expected_keywords}"
