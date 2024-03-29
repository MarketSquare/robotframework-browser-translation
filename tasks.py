import os

from invoke import task


@task
def lint(ctx, fix=False):
    print("Run mypy:")
    ctx.run("mypy --exclude .venv .")
    print("Run black:")
    ctx.run("black .")
    print("Run ruff:")
    ruff_cmd = "ruff check "
    if fix:
        ruff_cmd = f"{ruff_cmd} --fix"
    ctx.run(ruff_cmd)
    in_ci = os.getenv("GITHUB_WORKFLOW")
    print(f"Lint Robot files {'in ci' if in_ci else ''}")
    cmd = ["robotidy", "atest"]
    if in_ci:
        cmd.insert(1, "--check")
        cmd.insert(1, "--diff")
    ctx.run(" ".join(cmd))


@task
def utest(ctx):
    ctx.run("pytest .")


@task
def atest(ctx):
    ctx.run("robot -L debug --outputdir atest/output atest")
