"""
View handlers for main views
"""

from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator

from datetime import (datetime, timedelta)

from mango.models import Task


class DayListView(ListView):
    """
    ListView-based class for representing page with tasks
    """

    model = Task
    context_object_name = 'tasks'

    @method_decorator(login_required(login_url="/login"))
    def dispatch(self, request, *args, **kwargs):
        """
        Protect view with login_required
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super(DayListView, self).dispatch(request, *args, **kwargs)

    def get_template_names(self):
        """
        Get html page with template
        :return:
        """
        return "viewer/day.html"

    def get_queryset(self):
        """
        Custom query with today Tasks for current user
        :return:
        """
        current_user = self.request.user
        return \
            Task.objects\
                .filter(user=current_user,
                        date_start__date=datetime.today())\
                .order_by("-task_priority")

    def get_context_data(self, **kwargs):
        """
        Add custom context for usage in html template
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)

        running_task = get_running_task(self.request)

        if running_task is not None:
            context["running_task"] = running_task

        return context

    def turn_next_task(self, request, all_task, task):
        """
        Stop current running task and start the new task
        :param task: current user task
        :param request:
        :param all_task: list with all users task with right ordering
        :return:
        """
        next_task = None
        is_next_task = False
        print([a.task_name for a in all_task])
        for current_task in all_task:
            if is_next_task:
                next_task = current_task
                break
            if current_task.task_name == task.task_name:
                is_next_task = True

        if next_task is not None:
            print(next_task.task_name)
            next_task.is_running = True
            next_task.date_start = timezone.now()
            next_task.save()

        task.is_complete = True
        task.is_running = False
        task.date_finish = timezone.now()
        task.save()

    def post(self, request, *args, **kwargs):
        """
        Handle post request from page
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if request.POST.get("start") is not None:
            task_name = request.POST.get("start")
            task = Task.objects.filter(user=request.user,
                                       task_name=task_name)[0]
            task.is_running = True
            task.date_start = timezone.now()
            task.save()

        if request.POST.get("pause") is not None:
            task_name = request.POST.get("pause")
            task = Task.objects.filter(user=request.user,
                                       task_name=task_name)[0]
            task.duration += timezone.now() - task.date_start
            task.is_running = False
            task.save()

        if request.POST.get("stop") is not None:
            task_name = request.POST.get("stop")
            task = Task.objects.filter(user=request.user,
                                       task_name=task_name)[0]
            task.is_running = False
            task.date_finish = timezone.now()
            task.is_complete = True
            task.save()

        if request.POST.get("delete") is not None:
            task_name = request.POST.get("delete")
            task = Task.objects.filter(user=request.user,
                                       task_name=task_name)[0]
            task.delete()

        if request.POST.get("next") is not None:
            task_name = request.POST.get("next")
            task = Task.objects.filter(user=request.user,
                                       task_name=task_name)[0]
            all_task = \
                Task.objects\
                    .filter(user=request.user,
                            date_start__date=timezone.now(),
                            is_complete=False)\
                    .order_by("-task_priority")

            self.turn_next_task(request, all_task, task)

        if request.POST.get("previous") is not None:
            task_name = request.POST.get("previous")
            task = Task.objects.filter(user=request.user,
                                       task_name=task_name)[0]
            all_task = \
                Task.objects \
                    .filter(user=request.user,
                            date_start__date=timezone.now(),
                            is_complete=False) \
                    .order_by("task_priority")  # difference between code blocks

            self.turn_next_task(request, all_task, task)

        context = {"tasks": self.get_queryset()}
        running_task = get_running_task(request)

        if running_task is not None:
            context["running_task"] = running_task

        return render(request, "viewer/day.html", context)


class AccountView(DetailView):
    """
    DetailView-based class for display the page with current user
    """

    context_object_name = 'user'

    @method_decorator(login_required(login_url="/login"))
    def dispatch(self, request, *args, **kwargs):
        """
        Protect view with login_required
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super(AccountView, self).dispatch(request, *args, **kwargs)

    def get_template_names(self):
        """
        Get html page with template
        :return:
        """
        return "viewer/account.html"

    def get_object(self, queryset=None):
        """
        Get current request user
        :return:
        """
        return self.request.user

    def get_context_data(self, **kwargs):
        """
        Add custom context for usage in html template
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)

        running_task = get_running_task(self.request)

        if running_task is not None:
            context["running_task"] = running_task

        return context


class TasksView(ListView):
    """
    ListView-based class for display the page with all user's tasks
    """

    context_object_name = 'tasks'

    @method_decorator(login_required(login_url="/login"))
    def dispatch(self, request, *args, **kwargs):
        """
        Protect view with login_required
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super(TasksView, self).dispatch(request, *args, **kwargs)

    def get_template_names(self):
        """
        Get html page with template
        :return:
        """
        return "viewer/tasks.html"

    def get_queryset(self):
        """
        Custom query with all Tasks for current user
        :return:
        """
        current_user = self.request.user
        return \
            Task.objects\
                .filter(user=current_user)\
                .order_by("-task_priority")

    def get_context_data(self, **kwargs):
        """
        Add custom context for usage in html template
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)

        running_task = get_running_task(self.request)

        if running_task is not None:
            context["running_task"] = running_task

        return context

    def post(self, request, *args, **kwargs):
        """
        Handle post request from page
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if request.POST.get("start") is not None:
            task_name = request.POST.get("start")
            task = Task.objects.filter(user=request.user,
                                       task_name=task_name)[0]
            task.is_running = True
            task.date_start = timezone.now()
            task.save()

        if request.POST.get("delete") is not None:
            task_name = request.POST.get("delete")
            task = Task.objects.filter(user=request.user,
                                       task_name=task_name)[0]
            task.delete()

        context = {"tasks": self.get_queryset()}
        running_task = get_running_task(request)

        if running_task is not None:
            context["running_task"] = running_task

        return render(request, "viewer/day.html", context)


class Day:
    def __init__(self, date, number_of_tasks, total_priority):
        self.date = date
        self.number_of_tasks = number_of_tasks
        self.total_priority = total_priority


def main(request):
    """
    Main view with index page
    :param request:
    :return:
    """
    return render(request, "index.html", {})


def get_running_task(request):
    """
    Get only (!) one running task from database
    It's available for having multiply running tasks, but only
    one will be in the bottom navigation bar
    It may be fixed in the future
    :param request:
    :return: only one (!) running task if it exists, otherwise return None
    """
    current_user = request.user
    running_tasks = \
        Task.objects \
            .filter(user=current_user,
                    date_start__date=datetime.today(),
                    is_running=True)

    if len(running_tasks) > 0:
        print([t.task_name for t in running_tasks])
        return running_tasks[0]
    else:
        return None


@login_required(login_url="/login")
def day_add(request):
    """
    Page with the addition form for new tasks
    :param request:
    :return:
    """

    if request.method == "POST":
        task_name = request.POST.get("text")
        priority = request.POST.get("priority")
        if (task_name is not None) and (priority is not None):
            if len(Task.objects.filter(user=request.user,
                                       task_name=task_name,
                                       is_complete=False)) > 0:
                messages.error(request, "Task already exist")
                return render(request, "viewer/day_add.html", {})

            if request.POST.get("today") == "true":
                task = Task.objects.create(user=request.user,
                                           task_name=task_name,
                                           task_priority=priority,
                                           date_start=timezone.now())
            else:
                task = Task.objects.create(user=request.user,
                                           task_name=task_name,
                                           task_priority=priority)

            task.save()
            return HttpResponseRedirect(reverse("day"))
        else:
            messages.error(request, "Invalid fields")

    return render(request, "viewer/day_add.html", {})


@login_required(login_url="/login")
def calendar(request):
    """
    Page with the calendar with tasks, available only for authenticated users
    :param request:
    :return:
    """
    days = []

    user_tasks = Task.objects.filter(user=request.user).order_by("-date_start")

    dates = []
    delta = timedelta(days=1)

    number_of_showing_days = 30
    for day_index in range(number_of_showing_days):
        dates.append(datetime.today() + day_index * delta)

    for date in dates:
        day_tasks = user_tasks.filter(date_start__date=date)
        if len(day_tasks) > 0:
            total_priority = 0
            for task in day_tasks:
                total_priority += task.task_priority

            days.append(Day(date.strftime("%Y-%m-%d"),
                            len(day_tasks),
                            total_priority))

    context = {"days": days}

    running_task = get_running_task(request)
    if running_task is not None:
        context["running_task"] = running_task

    return render(request, "viewer/calendar.html", context)
