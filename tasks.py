
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

@task
def createsuperuser(ctx):
    ctx.run("python manage.py createsuperuser")

@task
def migrate(ctx):
    ctx.run("python manage.py migrate")

@task
def makemigrations(ctx):
    ctx.run("python manage.py makemigrations")

@task(makemigrations, migrate, createsuperuser)
def start(ctx):
    print("Done")
