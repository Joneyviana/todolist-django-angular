from rest_framework import serializers
from .models import Plan, Task


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id','name','plan')

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id','name','description','plan')

class PlanListSerializer(serializers.ModelSerializer):
    tasks = TaskListSerializer(many=True, read_only=True)
    class Meta:
        model = Plan
        fields = ('id','user','name','tasks')

class PlanSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    class Meta:
        model = Plan
        fields = ('id','user','name','tasks')
