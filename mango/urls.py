from django.urls import path

from mango import views
from mango.views import (DayListView, AccountView, TasksView)


urlpatterns = [
    path('', views.main, name='main'),
    path('day/', DayListView.as_view(), name='day'),
    path('add/', views.day_add, name='add'),
    path('month/', views.month, name='month'),
    path('tasks/', TasksView.as_view(), name='tasks'),
    path('account/', AccountView.as_view(), name='account')
]
