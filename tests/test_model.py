from django.test import TestCase
from django.contrib.auth.models import User

from datetime import timedelta

from mango.models import Task


class TaskTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(email="a@b", password="123")
        Task.objects.create(user=user, task_name="Meow", task_priority=5)

    def test_task_name_max_length(self):
        task = Task.objects.get(id=1)
        max_length = task._meta.get_field('task_name').max_length

        self.assertEquals(max_length, 100)

    def test_default_value(self):
        task = Task.objects.get(id=1)

        self.assertEquals(task.duration, timedelta(0))
        self.assertFalse(task.is_running)
        self.assertFalse(task.is_complete)
