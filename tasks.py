
from invoke import task, call

@task
def add(ctx):
    ctx.run("git add .")

@task(add)
def commit(ctx,msg):
    ctx.run("git commit -m'{{msg}}'".format(msg))

@task
def deploy(ctx, msg):
    add(ctx)
    commit(ctx, msg)
    ctx.run("git push origin master")
    ctx.run("git push heroku master")
