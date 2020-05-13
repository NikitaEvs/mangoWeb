from django.contrib.auth import views
from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.conf import settings

from accounts import views


urlpatterns = [
    path('login/', views.login, name='login'),
    path('reg/', views.register, name='reg'),
    path('logout/', LogoutView.as_view(), name='logout'),
]