"""
View handlers for main views
"""


from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def main(request):
    """
    Main view with index page
    :param request:
    :return:
    """
    return render(request, "index.html", {})


@login_required(login_url="/login")
def engine(request):
    """
    Page with main functionality, available only for authenticated users
    :param request:
    :return:
    """
    return render(request, "mango.html", {})
