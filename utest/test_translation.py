import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest

import robotframework_browser_translation

SUPPORTED_LANGUAGES = ("fi", "de")


def _language_map() -> dict[str, Path]:
    return {
        entry["language"]: Path(entry["path"])
        for entry in robotframework_browser_translation.get_language()
    }


@pytest.fixture(scope="module", params=SUPPORTED_LANGUAGES)
def language(request: pytest.FixtureRequest) -> str:
    return str(request.param)


@pytest.fixture(scope="module")
def translation_file(language: str) -> Path:
    return _language_map()[language]


@pytest.fixture(scope="module")
def data(translation_file: Path) -> robotframework_browser_translation.Language:
    with translation_file.open("r") as translation_stream:
        return json.load(translation_stream)


def test_translation():
    # Retrieve the list of supported languages
    langs = robotframework_browser_translation.get_language()
    lang_map = {entry["language"]: Path(entry["path"]) for entry in langs}

    # Verify that all expected languages are returned
    assert len(langs) == len(SUPPORTED_LANGUAGES)

    # Validate each configured language and translation file
    for lang in SUPPORTED_LANGUAGES:
        assert lang in lang_map
        translation_path = lang_map[lang]
        assert translation_path.name == f"translation_{lang}.json"
        assert translation_path.is_file()


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
        translated_name = data[translation]["name"]
        assert isinstance(translated_name, str), translation
        assert translated_name.strip(), translation


def test_keyword_names_no_space(data: robotframework_browser_translation.Language):
    for translation, value in data.items():
        assert " " not in translation, translation
        assert " " not in value["name"], value


def test_verify_checksum(translation_file: Path, tmp_path: Path):
    source_file = tmp_path / "translation.json"
    subprocess.run(
        [sys.executable, "-m", "Browser.entry", "translation", source_file],
        check=True,
    )
    with source_file.open("r") as source_translation:
        source_data = json.load(source_translation)
    with translation_file.open("r") as translation_stream:
        translation_data = json.load(translation_stream)
    for kw in source_data:
        source_sha256 = source_data[kw]["sha256"]
        translation_sha256 = translation_data[kw]["sha256"]
        assert source_sha256 == translation_sha256, (
            f"{kw} sha256 was {source_sha256} expected {translation_sha256}"
        )
