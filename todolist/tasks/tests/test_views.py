from django.test import RequestFactory
from test_plus.test import TestCase
from django.core.urlresolvers import reverse
from django.test import Client
from ..views import TemplatePlanView
from .factories import *
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from ..models import Plan, Task
from todolist.users.models import User

class TemplatePlanViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get(reverse('dashboard:home'))
    
    def test_get_with_user(self):
        self.user = self.make_user()
        self.request.user = self.user
        self.plan = Plan.objects.create(user=self.user, name="My Plan")
        response = TemplatePlanView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "tasks/plan_list.html")
    
    def test_get_without_user(self):
        with self.assertRaisesMessage(AttributeError, "'WSGIRequest' object has no attribute 'user'"):
           response = TemplatePlanView.as_view()(self.request)

class CreatePlanTest(APITestCase):
    
    def testCreatePlan(self):
        self.user = User.objects.create(username="Jão")
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        url = reverse('dashboard:api-list')
        data = {"name":"nomeQualquer","tasks":[]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Plan.objects.count(), 1)
        self.assertEqual(Plan.objects.get().name, 'nomeQualquer')
        
class PlanTests(APITestCase):    
    def setUp(self):
        self.user = User.objects.create(username="Jão")
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.plan = Plan.objects.create(name="nomeQualquer",user=self.user)
        self.plan.save()
    
    def testRetrievePlan(self):
        url = reverse('dashboard:api-list')
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = '[{"id":%s,"user":%s,"name":"nomeQualquer","tasks":[]}]'%(self.plan.id,self.plan.user.id)
        self.assertEqual(response.content.decode("utf-8"), content)
    
    def testDeletePlan(self):
        
        url = reverse('dashboard:api-delete',kwargs={'pk':self.plan.id})
        self.client.delete(url, format='json')
        self.assertEqual(Plan.objects.count(), 0)

    def testPostTask(self):
        url = reverse('dashboard:api-taskpost')
        data = {"name":"nomeQualquer",'plan':self.plan.id}
        response = self.client.post(url, data, format='json')        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        url = reverse('dashboard:api-taskpost')
        data = {"name":"nomeQualquer",'plan':self.plan.id+1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def testDeleteTask(self):
        task = self.plan.tasks.create(description="Qualquer")
        self.assertEqual(Task.objects.count(), 1)
        url = reverse('dashboard:api-taskdelete',kwargs={'pk':task.pk})
        response = self.client.delete(url,format='json')        
        self.assertEqual(Task.objects.count(), 0)
    
    

        

           
