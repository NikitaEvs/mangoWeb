"""
Views handler for auth pages
"""


from django.contrib.auth import (login as auth_login,  authenticate)
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User


def login(request):
    """
    Login handler for sign in page
    :param request:
    :return:
    """

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("day"))

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)

                if not request.POST.get("remember-me", None):
                    request.session.set_expiry(0)

                return HttpResponseRedirect(reverse("day"))
            else:
                message = "Your account is not activated"
        else:
            message = "Incorrect email or/and login"

        if message is not None:
            messages.error(request, message)

    return render(request, "registration/login.html", {})


def register(request):
    """
    Registration handler for sign up page
    :param request:
    :return:
    """

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        repeated_password = request.POST.get("secondPassword")
        message = None

        if password != repeated_password:
            message = "Passwords are different"

        if User.objects.filter(username=email).exists():
            message = "Already exist account with this email"

        if message is not None:
            messages.error(request, message)
        else:
            user = User.objects.create_user(username=email,
                                            password=password)
            user.is_superuser = False
            user.is_staff = False
            user.save()
            return HttpResponseRedirect(reverse("login"))

    return render(request, "registration/reg.html", {})
