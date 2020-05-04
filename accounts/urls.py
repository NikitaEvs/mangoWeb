from django.contrib.auth import views
from django.urls import path
from accounts import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('login/', views.login, name='login'),
    path('reg/', views.register, name='reg'),
]