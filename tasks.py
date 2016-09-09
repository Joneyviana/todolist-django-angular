
from invoke import task

@task
def add(ctx):
    ctx.run("git add .")

