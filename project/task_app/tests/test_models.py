from django.test import TestCase
from task_app.models import TaskUser
from core_app.models import UserProfile
from task_app.tests.mocks.mock_user import mock_user_profile
from task_app.tests.mocks.mock_task import mock_task
from task_app.serializers import TaskSerializer


class TaskUserModelTestCase(TestCase):

    def test_create_task(self):
        """Crete new task"""
        self.user = mock_user_profile()
        self.task = mock_task(user=self.user)
        self.assertEqual(self.user, self.task.user)
