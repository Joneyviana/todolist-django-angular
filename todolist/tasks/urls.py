from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # URL pattern for the UserListView
    url(
        regex=r'^$',
        view=views.TemplatePlanView.as_view(),
        name='home'
    ),
      url(
        regex=r'^api/plans$',
        view=views.PlanListAPIView.as_view(),
        name='api-list'
    ),
    url(
        regex=r'^api/plan/(?P<name>\w+)$',
        view=views.PlanRetrieveView.as_view(),
        name='api-list'
    ),
    url(
        regex=r'^api/(?P<pk>\d+)$',
        view=views.PlanUpdateDeleteAPIView.as_view(),
        name='api-delete'
    ),
     url(
        regex=r'^api/task$',
        view=views.TaskPostAPIView.as_view(),
        name='api-taskpost'
    ),
     url(
        regex=r'^api/task/(?P<pk>\d+)$',
        view=views.TaskDeleteUpdateAPIView.as_view(),
        name='api-taskdelete'
    ),
  ]
  
