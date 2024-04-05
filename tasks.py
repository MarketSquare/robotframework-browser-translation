import os
import shutil
from pathlib import Path

from invoke import task

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
    print("Run mypy:")
    ctx.run("mypy --exclude .venv .")
    print("Run black:")
    black_cmd = ["black", "."]
    if in_ci:
        black_cmd.insert(1, "--check")
    ctx.run(" ".join(black_cmd))
    print("Run ruff:")
    ruff_cmd = "ruff check "
    if fix:
        ruff_cmd = f"{ruff_cmd} --fix"
    ctx.run(ruff_cmd)
    print(f"Lint Robot files {'in ci' if in_ci else ''}")
    cmd = ["robotidy", "atest"]
    if in_ci:
        cmd.insert(1, "--check")
        cmd.insert(1, "--diff")
    ctx.run(" ".join(cmd))


@task
def utest(ctx):
    ctx.run("python -m pytest .")


@task
def atest(ctx):
    ctx.run("python -m robot -L debug --outputdir atest/output atest")


@task
def clean(ctx):
    for target in [
        DIST_DIR,
        ATEST_OUTPUT,
        RUFF_CACHE,
        PYTEST_CACHE,
        MYPY_CACHE,
        BUILD_DIR,
    ]:
        print(target)
        if target.exists():
            shutil.rmtree(target)
