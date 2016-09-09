import  factory
from ..models import  Plan
from ..models import Task


class PlanFactory(factory.Factory):
    class Meta:
        model = Plan

    name = "My plan"


class TaskFactory(factory.Factory):
    class Meta:
        model = Task

    
    
    plan = factory.SubFactory(PlanFactory)
    description = "my Task"
    id = 2

