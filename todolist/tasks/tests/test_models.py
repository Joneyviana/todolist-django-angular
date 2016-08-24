
from test_plus.test import TestCase
from .factories import *
from ..models import Task
from ..models import Plan
class TestTask(TestCase):

    def setUp(self):
        #self.plan = Plan.objects.create(name="my Plan")
        #self.task = Task.objects.create(description="my Task",plan=self.plan)
        self.task = TaskFactory.create()
    def test__str__(self):
        self.assertEqual(
            self.task.description,
            "my Task"  # This is the default username for self.make_user()
        )

    def test_with_plan(self):
        self.assertTrue(isinstance(self.task.plan,Plan))