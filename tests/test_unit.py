from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from mango.models import Task
from mango.views import get_running_task


class EngineUnit(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="cat", password="meow")
        user.save()
        task = Task.objects.create(user=user,
                                   task_name="do",
                                   task_priority=1,
                                   date_start=timezone.now(),
                                   is_running=True)

        another_task = Task.objects.create(user=user,
                                           task_name="something",
                                           task_priority=2)

        task.save()
        another_task.save()

    def test_get_running(self):
        self.client.login(username="cat", password="meow")
        request = self.client.get("/day/")
        request.user = User.objects.get(username="cat")

        task = get_running_task(request)
        self.assertEquals(task.task_name, "do")
