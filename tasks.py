import os
from invoke import task, call

@task
def staticfile(ctx):
    if not os.path.exists("staticfiles"):
        ctx.run("python manage.py collectstatic")

@task
def add(ctx):
    ctx.run("git add .")

@task
def commit(ctx,msg):
    ctx.run("git commit -m'{0}'".format(msg))

@task(staticfile, add)
def deploy(ctx, msg):
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
