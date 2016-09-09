
from invoke import task, call

@task
def add(ctx):
    ctx.run("git add .")

@task(add)
def commit(ctx,msg):
    ctx.run("git commit -m'{{msg}}'".format(msg))

@task(pre=[call(commit, msg="new commit")])
def deploy(ctx):
    ctx.run("git push origin master")
    ctx.run("git push heroku master")
