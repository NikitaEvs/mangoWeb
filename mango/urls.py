from django.urls import path
from mango import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', views.main, name='main'),
    path('mango/', views.engine, name='mango')
]