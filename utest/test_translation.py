import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest

from robotframework_browser_translation import get_language, translation_files

# The languages this package promises to ship. Every other test derives its
# languages from get_language(), so a new language is picked up automatically;
# this tuple only guards against discovery silently finding nothing.
EXPECTED_LANGUAGES = ("de", "fi")


@pytest.fixture(scope="module", params=sorted(translation_files()))
def language(request: pytest.FixtureRequest) -> str:
    return str(request.param)


@pytest.fixture(scope="module")
def translation_file(language: str) -> Path:
    return translation_files()[language]


@pytest.fixture(scope="module")
def data(translation_file: Path) -> dict:
    return json.loads(translation_file.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def source_data(tmp_path_factory: pytest.TempPathFactory) -> dict:
    """Keyword specification of the installed Browser library.

    Generated once per session, because every drift test compares against it.
    """
    source_file = tmp_path_factory.mktemp("browser") / "translation.json"
    subprocess.run(
        [sys.executable, "-m", "Browser.entry", "translation", source_file],
        check=True,
    )
    return json.loads(source_file.read_text(encoding="utf-8"))


def test_translation():
    lang_map = {entry["language"]: Path(entry["path"]) for entry in get_language()}
    assert tuple(sorted(lang_map)) == EXPECTED_LANGUAGES
    for lang, translation_path in lang_map.items():
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


def test_keyword_names_no_space(data: dict):
    for translation, value in data.items():
        assert " " not in translation, translation
        assert " " not in value["name"], value


def test_no_untranslated_keywords(data: dict, source_data: dict, language: str):
    missing = sorted(set(source_data) - set(data))
    assert not missing, (
        f"{len(missing)} keyword(s) of the Browser library are missing from the "
        f"'{language}' translation: {missing}"
    )


def test_no_obsolete_keywords(data: dict, source_data: dict, language: str):
    obsolete = sorted(set(data) - set(source_data))
    assert not obsolete, (
        f"{len(obsolete)} keyword(s) in the '{language}' translation no longer "
        f"exist in the Browser library: {obsolete}"
    )


def test_verify_checksum(data: dict, source_data: dict, language: str):
    outdated = sorted(
        keyword
        for keyword in set(source_data) & set(data)
        if source_data[keyword]["sha256"] != data[keyword]["sha256"]
    )
    assert not outdated, (
        f"{len(outdated)} keyword(s) have '{language}' documentation that is out "
        f"of date with the Browser library: {outdated}"
    )
