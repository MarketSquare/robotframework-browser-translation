import json
from collections import Counter
from pathlib import Path

import pytest

import robotframework_browser_translation_fi


@pytest.fixture(scope="module")
def data() -> robotframework_browser_translation_fi.Language:
    lang = robotframework_browser_translation_fi.get_language()
    result_path = Path(lang["path"])
    with result_path.open("r") as file:
        return json.load(file)


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


def test_json_file_format(data: dict):
    for translation in data.values():
        assert translation.get("name"), translation
        assert translation.get("doc"), translation


def test_keywords_are_unique(data: dict):
    kw_names = [translation.get("name") for translation in data.values()]
    duplicates = {}
    for key, value in dict(Counter(kw_names)).items():
        if value != 1:
            duplicates[key] = value
    assert len(kw_names) == len(set(kw_names)), duplicates


def test_keyword_names_are_unique(data: dict):
    for translation in data:
        if translation in ["http", "__init__", "__intro__"]:
            continue
        assert (
            translation != data[translation]["name"]
        ), f"{translation} == {data[translation]['name']}"


def test_keyword_names_no_space(data: robotframework_browser_translation_fi.Language):
    for translation, value in data.items():
        assert " " not in translation, translation
        assert " " not in value["name"]
