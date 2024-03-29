import os

from invoke import task


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
    ctx.run("robot -L debug --outputdir atest/output atest")
