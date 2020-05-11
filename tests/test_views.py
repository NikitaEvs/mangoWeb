from django.test import TestCase
from django.contrib.auth.models import User

from mango.models import Task

from django.utils import timezone


class AuthViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="cat", password="meow")
        user.save()

    def test_nonuser_access_login(self):
        response = self.client.get("/login/")

        self.assertEqual(response.status_code, 200)

    def test_nonuser_access_reg(self):
        response = self.client.get("/reg/")

        self.assertEqual(response.status_code, 200)

    def test_nonuser_access_logout(self):
        response = self.client.get("/logout/")

        self.assertRedirects(response, "/")

    def test_nonuser_access_index(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

    def test_user_access_login(self):
        self.client.login(username="cat", password="meow")
        response = self.client.get("/login/")

        self.assertRedirects(response, "/day/")

    def test_user_access_reg(self):
        response = self.client.get("/reg/")
        self.client.login(username="cat", password="meow")

        self.assertEqual(response.status_code, 200)

    def test_user_access_logout(self):
        response = self.client.get("/logout/")
        self.client.login(username="cat", password="meow")

        self.assertRedirects(response, "/")

    def test_user_access_index(self):
        response = self.client.get("/")
        self.client.login(username="cat", password="meow")

        self.assertEqual(response.status_code, 200)

    def test_nonuser_access_account(self):
        response = self.client.get("/account/")

        self.assertRedirects(response, "/login?next=/account/",
                             status_code=302,
                             target_status_code=301)

    def test_nonuser_access_month(self):
        response = self.client.get("/month/")

        self.assertRedirects(response, "/login?next=/month/",
                             status_code=302,
                             target_status_code=301)

    def test_nonuser_access_day(self):
        response = self.client.get("/day/")

        self.assertRedirects(response, "/login?next=/day/",
                             status_code=302,
                             target_status_code=301)

    def test_nonuser_access_day_add(self):
        response = self.client.get("/add/")

        self.assertRedirects(response, "/login?next=/add/",
                             status_code=302,
                             target_status_code=301)

    def test_nonuser_access_tasks(self):
        response = self.client.get("/tasks/")

        self.assertRedirects(response, "/login?next=/tasks/",
                             status_code=302,
                             target_status_code=301)

    def test_login(self):
        response = self.client.post("/login/",
                                    {"email": "cat", "password": "meow"})

        self.assertRedirects(response, "/day/",
                             status_code=302,
                             target_status_code=200)

    def test_reg(self):
        response = self.client.post("/reg/",
                                    {"email": "a@b",
                                     "password": "pass",
                                     "secondPassword": "pass"})

        self.assertRedirects(response, "/login/",
                             status_code=302,
                             target_status_code=200)

    def test_login_failed(self):
        response = self.client.post("/login/",
                                    {"email": "cat", "password": "awww"})

        self.assertEqual(response.status_code, 200)

    def test_reg_failed(self):
        response = self.client.post("/reg/",
                                    {"email": "cat",
                                     "password": "pass",
                                     "secondPassword": "pass"})

        self.assertEqual(response.status_code, 200)


class TaskViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="cat", password="meow")
        user.save()

        task = Task.objects.create(user=user, task_name="do", task_priority=1)
        task.save()

    def test_long_name(self):
        self.client.login(username="cat", password="meow")
        response = self.client.post("/add/", {
            "text": "a" * 150,
            "priority": 5,
            "date": timezone.now().strftime("%Y-%m-%d")
        })

        self.assertEquals(response.status_code, 200)

    def test_wrong_date(self):
        self.client.login(username="cat", password="meow")
        response = self.client.post("/add/", {
            "text": "a" * 150,
            "priority": 5,
            "date": "oops"
        })

        self.assertEquals(response.status_code, 200)

    def test_successfully_create(self):
        self.client.login(username="cat", password="meow")
        response = self.client.post("/add/", {
            "text": "new",
            "priority": 5,
            "date": timezone.now().strftime("%Y-%m-%d")
        })

        self.assertRedirects(response, "/day/",
                             status_code=302,
                             target_status_code=200)

    def test_month(self):
        self.client.login(username="cat", password="meow")
        response = self.client.get("/month/")

        self.assertEqual(response.status_code, 200)


class TasksListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="cat", password="meow")
        user.save()

        Task.objects.create(user=user, task_name="do", task_priority=1).save()
        Task.objects.create(user=user, task_name="del", task_priority=1).save()

    def test_start(self):
        self.client.login(username="cat", password="meow")

        task = Task.objects.get(task_name="do")

        response = self.client.post("/tasks/", {
            "start": task.id
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.get(task_name="do").is_running)

    def test_delete(self):
        self.client.login(username="cat", password="meow")

        task = Task.objects.get(task_name="del")

        response = self.client.post("/tasks/", {
            "delete": task.id
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.all().count(), 1)


class AccountViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="cat", password="meow")
        user.save()

    def test_access(self):
        self.client.login(username="cat", password="meow")

        response = self.client.get("/account/")

        self.assertEqual(response.status_code, 200)


class DayListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="cat", password="meow")
        user.save()

        Task.objects.create(user=user,
                            task_name="start",
                            task_priority=1).save()

        Task.objects.create(user=user,
                            task_name="pause",
                            task_priority=1,
                            is_running=True,
                            date_start=timezone.now()).save()

        Task.objects.create(user=user,
                            task_name="stop",
                            task_priority=1,
                            is_running=True).save()

        Task.objects.create(user=user,
                            task_name="delete",
                            task_priority=1).save()

        Task.objects.create(user=user,
                            task_name="previous",
                            task_priority=5,
                            date_start=timezone.now()).save()

        Task.objects.create(user=user,
                            task_name="current",
                            task_priority=3,
                            date_start=timezone.now()).save()

        Task.objects.create(user=user,
                            task_name="next",
                            task_priority=2,
                            date_start=timezone.now()).save()

    def test_start(self):
        self.client.login(username="cat", password="meow")

        task = Task.objects.get(task_name="start")

        response = self.client.post("/day/", {
            "start": task.id
        })

        task = Task.objects.get(task_name="start")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(task.is_running)

    def test_pause(self):
        self.client.login(username="cat", password="meow")

        task = Task.objects.get(task_name="pause")

        response = self.client.post("/day/", {
            "pause": task.id
        })

        task = Task.objects.get(task_name="pause")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(task.is_running)

    def test_stop(self):
        self.client.login(username="cat", password="meow")

        task = Task.objects.get(task_name="stop")

        response = self.client.post("/day/", {
            "stop": task.id
        })

        task = Task.objects.get(task_name="stop")

        self.assertEqual(response.status_code, 200)

        self.assertFalse(task.is_running)
        self.assertTrue(task.is_complete)

    def test_delete(self):
        self.client.login(username="cat", password="meow")

        task = Task.objects.get(task_name="delete")

        response = self.client.post("/day/", {
            "delete": task.id
        })

        self.assertEqual(response.status_code, 200)

        deleted = Task.objects.filter(task_name="delete")

        self.assertEqual(len(deleted), 0)

    def test_previous(self):
        self.client.login(username="cat", password="meow")

        task = Task.objects.get(task_name="current")

        response = self.client.post("/day/", {
            "previous": task.id
        })

        task = Task.objects.get(task_name="current")

        self.assertEqual(response.status_code, 200)

        new_current = Task.objects.get(task_name="previous")

        self.assertTrue(new_current.is_running)
        self.assertFalse(task.is_running)

    def test_next(self):
        self.client.login(username="cat", password="meow")
        task = Task.objects.get(task_name="current")

        response = self.client.post("/day/", {
            "next": task.id
        })

        task = Task.objects.get(task_name="current")

        self.assertEqual(response.status_code, 200)

        new_current = Task.objects.get(task_name="next")

        self.assertTrue(new_current.is_running)
        self.assertFalse(task.is_running)


class MonthViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="cat", password="meow")
        user.save()

        Task.objects.create(user=user,
                            task_name="do",
                            task_priority=1,
                            date_start=timezone.now())

    def test_show(self):
        self.client.login(username="cat", password="meow")

        response = self.client.post("/month/", {
            "request_day": timezone.now().strftime("%Y-%m-%d")
        })

        self.assertEqual(response.status_code, 200)
