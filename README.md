# Robot Framework Browser Translation (Finnish + German)
[![Version](https://img.shields.io/pypi/v/robotframework-browser-translation.svg)](https://pypi.python.org/pypi/robotframework-browser-translation)
![CI](https://github.com/MarketSquare/robotframework-browser-translation/actions/workflows/on-push.yml/badge.svg)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![All Contributors](https://img.shields.io/github/all-contributors/MarketSquare/robotframework-browser-translation?color=ee8449&style=flat-square)](#contributors)


This project provides language translations for the Robot Framework
[Browser](https://github.com/MarketSquare/robotframework-browser) library.

Currently supported languages:

- Finnish (`fi`) via `translation_fi.json`
- German (`de`) via `translation_de.json`

The package is discovered by Browser through Python plugin naming conventions
(`robotframework_browser_translation`) and exposes `get_language()` with available
translation files.

This project uses Browser library
[Python plugin API](https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/)
to provide
translation files for the Browser library. The `get_language()` method returns a
list of dictionaries like this:

```python
[
  {"language": "fi", "path": "/path/to/translation_fi.json"},
  {"language": "de", "path": "/path/to/translation_de.json"},
]
```

Browser uses these values to select the requested language when Browser is imported.

## Use In Robot Framework

Install the translation package (and Browser, if not installed yet):

```bash
pip install robotframework-browser robotframework-browser-translation
```

Then choose the language in the Browser import:

```robotframework
*** Settings ***
Library    Browser    language=fi
```

or:

```robotframework
*** Settings ***
Library    Browser    language=de
```

## Developer Setup With UV

This repository includes `uv` in development requirements. A common local setup is:

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
uv pip install -r requirements-dev.txt
```

Run checks/tests:

```bash
uv run invoke utest
uv run invoke lint
```

## Add A New Language (Developer Workflow)

1. Create a new translation file from Browser's current keywords:

```bash
uv run python -m Browser.entry translation robotframework_browser_translation/translation_xx.json
```

2. Translate values in `name` and `doc` fields in `translation_xx.json`.
3. Keep `sha256` values as generated (they are used to detect upstream doc changes).
4. Register the new language in `robotframework_browser_translation/__init__.py` inside `get_language()`.
5. Verify checksums and test suite:

```bash
uv run invoke utest
```

Optional checksum comparison against current Browser docs:

```bash
uv run rfbrowser translation --compare robotframework_browser_translation/translation_xx.json
```

## Pytest Quickstart For This Project

This project keeps Python unit tests in [utest/test_translation.py](utest/test_translation.py).

Useful commands:

```bash
uv run invoke utest
uv run pytest -q
uv run pytest -k checksum -q
```

How pytest works here:

- Test discovery: pytest collects functions whose names start with `test_`.
- Fixtures: reusable setup blocks (`language`, `translation_file`, `data`) provide test inputs.
- Parametrization: the `language` fixture runs dependent tests once per language (`fi`, `de`).
- Assertion style: plain `assert ...` statements are enough; pytest prints useful failure diffs.

Tip:

If you add a new language, add its code to `SUPPORTED_LANGUAGES` in [utest/test_translation.py](utest/test_translation.py) so the same checks run automatically.

## Detect changes in documentation
Each `translation_xx.json` contains a `sha256` value for every keyword. The
checksum is generated from the original Browser library documentation and is
used to detect outdated or missing translations.

Use:

`rfbrowser translation --compare robotframework_browser_translation/translation_xx.json`

The command prints keywords that are missing from the translation file or need
to be updated.

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/aaltat"><img src="https://avatars.githubusercontent.com/u/2665023?v=4?s=100" width="100px;" alt="Tatu Aalto"/><br /><sub><b>Tatu Aalto</b></sub></a><br /><a href="#code-aaltat" title="Code">💻</a> <a href="#doc-aaltat" title="Documentation">📖</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
