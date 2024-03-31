import json
from pathlib import Path

import robotframework_browser_translation_fi


def test_translation():
    lang = robotframework_browser_translation_fi.get_language()
    expexted_path = (
        Path(__file__).parent.parent
        / "robotframework_browser_translation_fi"
        / "translation.json"
    )
    assert lang["language"] == "fi"
    result_path = Path(lang["path"])
    assert result_path == expexted_path
    assert result_path.is_file()


def test_json_file_format():
    lang = robotframework_browser_translation_fi.get_language()
    result_path = Path(lang["path"])
    with result_path.open("r") as file:
        data = json.load(file)
    for translation in data.values():
        assert translation.get("name"), translation
        assert translation.get("doc"), translation


def test_keywords_are_unique():
    lang = robotframework_browser_translation_fi.get_language()
    result_path = Path(lang["path"])
    with result_path.open("r") as file:
        data = json.load(file)
    kw_names = [translation.get("name") for translation in data.values()]
    assert len(kw_names) == len(set(kw_names))
