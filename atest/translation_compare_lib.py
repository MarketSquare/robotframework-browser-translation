import json
from pathlib import Path

from robot.api import logger

from robotframework_browser_translation import translation_files


def compare_translations(file: Path, language: str = "fi"):
    translations = translation_files()
    try:
        translation_file = translations[language.lower()]
    except KeyError:
        raise AssertionError(
            f"Unsupported language '{language}'. Supported languages are: "
            f"{sorted(translations)}."
        ) from None
    expected_data = json.loads(translation_file.read_text(encoding="utf-8"))
    expected_keywords = [kw["name"] for kw in expected_data.values()]
    logger.info(f"expected_keywords: {expected_keywords}")
    data = json.loads(Path(file).read_text(encoding="utf-8"))
    for keyword in data["keywords"]:
        logger.info(keyword)
        name = keyword["name"].replace(" ", "_").lower()
        assert name in expected_keywords, (
            f"name '{name}' not in expected keywords for language '{language}'"
        )
