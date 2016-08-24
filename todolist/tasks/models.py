from django.db import models
from ..users.models import User
# Create your models here.

class Plan(models.Model):
	
	name = models.CharField(max_length=50)
	user = models.ForeignKey(User, related_name='plans')

class Task(models.Model):
	name =  models.CharField(max_length=50)
	description = models.TextField(blank=True)
	plan = models.ForeignKey(Plan, related_name='tasks')

class Annotation(models.Model):
	
	description = models.TextField(default='')
	task = models.ForeignKey(Task, related_name='Annotations',blank=True)