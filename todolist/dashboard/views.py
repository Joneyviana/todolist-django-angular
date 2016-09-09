from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .models import Plan, Task
from .serializers import PlanListSerializer, PlanSerializer, TaskListSerializer,TaskSerializer
from rest_framework import mixins
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

def getUserPlans(request):
   
    return request.user.plans.all()

class PlanListAPIView(generics.ListCreateAPIView):
    
    serializer_class = PlanListSerializer
    
    def get_queryset(self):
        return getUserPlans(self.request)

    def post(self, request, *args, **kwargs):
        request.data["user"] = request.user.pk
        return self.create(request, *args, **kwargs)
    
class PlanUpdateDeleteAPIView(generics.DestroyAPIView):
    serializer_class = PlanListSerializer
    
    def get_queryset(self):
        return getUserPlans(self.request)

class TaskPostAPIView(mixins.CreateModelMixin,
                  generics.GenericAPIView):
    
    serializer_class = TaskListSerializer
    
    def post(self, request, *args, **kwargs):
       
        plan_id = request.data['plan'] 
        plan = Plan.objects.filter(pk=plan_id, user=request.user.pk)
        if plan:
            return self.create(request, *args, **kwargs)
        
        return Response(status=status.HTTP_403_FORBIDDEN)

class TaskDeleteUpdateAPIView(generics.DestroyAPIView,
                                   mixins.UpdateModelMixin):
    
    serializer_class = TaskSerializer
    def get_queryset(self):
        plans = getUserPlans(self.request)
        return Task.objects.filter(plan__in=plans)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class PlanRetrieveView(generics.RetrieveAPIView):
    serializer_class = PlanSerializer
    def get_object(self):
        plan = get_object_or_404(Plan.objects.all(),name=self.kwargs["name"])
        return plan 

class TemplatePlanView(LoginRequiredMixin,TemplateView):
   template_name = "dashboard/plan_list.html"
    