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
