"""
Models for Task system engine
"""


from django.db import models
from django.contrib.auth.models import User

from datetime import timedelta


class Task(models.Model):
    """
    Specific task with time's fields. Consist in relation many-to-one with
    AbstractTask and User
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100)
    task_priority = models.IntegerField(default=None, blank=True, null=True)
    duration = models.DurationField(default=timedelta(0), blank=True, null=True)
    date_start = models.DateTimeField(default=None, blank=True, null=True)
    date_finish = models.DateTimeField(default=None, blank=True, null=True)
    is_running = models.BooleanField(default=False, blank=True, null=True)
    is_complete = models.BooleanField(default=False, blank=True, null=True)
