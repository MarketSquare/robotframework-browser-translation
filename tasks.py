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


@task
def utest(ctx):
    ctx.run("pytest .")
