import os
import shutil
from dataclasses import fields
from importlib.metadata import version
from pathlib import Path

from invoke import task

import translation_tools
from robotframework_browser_translation import translation_files

ROOT_FOLDER = Path(__file__).parent.absolute()
ATEST_OUTPUT = ROOT_FOLDER / "atest" / "output"
DIST_DIR = ROOT_FOLDER / "dist"
RUFF_CACHE = ROOT_FOLDER / ".ruff_cache"
PYTEST_CACHE = ROOT_FOLDER / ".pytest_cache"
MYPY_CACHE = ROOT_FOLDER / ".mypy_cache"
BUILD_DIR = ROOT_FOLDER / "build"


@task
def lint(ctx, fix=False):
    in_ci = os.getenv("GITHUB_WORKFLOW")
    print("Run ruff format:")
    ruff_format = ["ruff", "format", "."]
    if in_ci:
        ruff_format.insert(2, "--check")
    ctx.run(" ".join(ruff_format))
    print("Run ruff check:")
    ruff_cmd = "ruff check "
    if fix and not in_ci:
        ruff_cmd = f"{ruff_cmd} --fix"
    ctx.run(ruff_cmd)
    print(f"Format Robot files {'in ci' if in_ci else ''}")
    cmd = ["robocop", "format"]
    if in_ci:
        cmd.extend(["--check", "--diff"])
    cmd.append("atest")
    ctx.run(" ".join(cmd))
    print("Run mypy:")
    ctx.run("mypy --exclude .venv .")


@task
def utest(ctx):
    ctx.run("python -m pytest .")


@task
def atest(ctx):
    ctx.run("python -m robot -L debug --outputdir atest/output atest")


def _languages(language: str | None) -> dict[str, Path]:
    files = translation_files()
    return {language: files[language]} if language else files


def _target(target: str | None) -> str:
    return target or version("robotframework-browser")


@task(
    help={
        "baseline": "Browser version the translations are currently in sync with.",
        "target": "Browser version to update to. Defaults to the installed one.",
    }
)
def changes(ctx, baseline, target=None):
    result = translation_tools.compare_releases(
        baseline, _target(target), _languages(None)
    )
    for category in fields(result):
        value = getattr(result, category.name)
        if isinstance(value, list):
            print(f"{category.name} ({len(value)}): {', '.join(value)}")
    for language, keywords in result.off_baseline.items():
        print(f"{language} not at baseline ({len(keywords)}): {', '.join(keywords)}")
    print(f"diffs: {result.diff_dir}")


@task(
    help={
        "language": "Language code. Defaults to every language.",
        "target": "Browser version to validate against. Defaults to the installed one.",
        "warnings": "Also print warnings.",
    }
)
def validate(ctx, language=None, target=None, warnings=False):
    english = translation_tools.spec(_target(target))
    errors = 0
    for code, path in _languages(language).items():
        for key, problems in translation_tools.validate(path, english).items():
            shown = [p for p in problems if warnings or translation_tools.is_error(p)]
            errors += sum(map(translation_tools.is_error, problems))
            for problem in shown:
                print(f"{code} {key}: {problem}")
    if errors:
        raise SystemExit(f"{errors} error(s)")


@task(
    help={
        "keywords": "Comma separated keywords whose checksum to take from the spec.",
        "language": "Language code. Defaults to every language.",
        "target": "Browser version to sync to. Defaults to the installed one.",
    }
)
def sync_checksums(ctx, keywords, language=None, target=None):
    english = translation_tools.spec(_target(target))
    keys = [key.strip() for key in keywords.split(",") if key.strip()]
    files = {
        path: translation_tools.read_entries(path)
        for path in _languages(language).values()
    }
    unknown = sorted(
        {key for key in keys if key not in english}
        | {key for entries in files.values() for key in keys if key not in entries}
    )
    if unknown:
        raise SystemExit(f"Unknown keyword(s): {', '.join(unknown)}")
    for path, entries in files.items():
        translation_tools.write_entries(
            path,
            {key: {**entries[key], "sha256": english[key]["sha256"]} for key in keys},
        )


@task
def clean(ctx):
    for target in [
        DIST_DIR,
        ATEST_OUTPUT,
        RUFF_CACHE,
        PYTEST_CACHE,
        MYPY_CACHE,
        BUILD_DIR,
        translation_tools.WORK_DIR,
    ]:
        print(target)
        if target.exists():
            shutil.rmtree(target)
