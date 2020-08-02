from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from task_app.tests.mocks.mock_task import mock_task
from task_app.tests.mocks.mock_user import mock_user_profile

TASK_LIST_CREATE_URL = reverse("task_app:list-create-task")


def detail_update_task(task):
    return reverse("task_app:retrieve-update-task", kwargs={"pk": task.id})


class PublicTaskUserAPIViewTestCase(TestCase):
    """ Test Case for public task API"""

    def setUp(self):
        self.client = APIClient()

    def test_unauthorized_get_list_task(self):
        """Test that return list task, but in this case return unauthorized"""
        res = self.client.get(TASK_LIST_CREATE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTaskUserAPIViewTestCase(TestCase):
    """ Test Case for private task API"""

    def setUp(self):
        self.client = APIClient()

        self.user_1 = mock_user_profile(email="test_1@gmail.com")
        self.task_1 = mock_task(name="task_1", user=self.user_1)
        self.task_2 = mock_task(name="task_2", user=self.user_1)

        self.user_2 = mock_user_profile(email="test_2@gmail.com")
        self.task_3 = mock_task(name="task_3", user=self.user_2)
        self.task_4 = mock_task(name="task_4", user=self.user_2)

        self.client.force_authenticate(self.user_1)

    def test_get_list_task_successfully(self):
        """Test that return successfully list task"""
        res = self.client.get(TASK_LIST_CREATE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 4)

    def test_create_task_successfully(self):
        """Test that creates a task and is assigned by the registered user"""
        data = {
            "name": "Create_name",
            "description": "description_test",
        }

        res = self.client.post(TASK_LIST_CREATE_URL, data=data, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", res.data)
        self.assertIn("description", res.data)
        self.assertIn("accept", res.data)

    def test_retrieve_task(self):
        """Test that retrieves task information"""
        data = {
            "name": "Change"
        }
        url = detail_update_task(self.task_1)

        res = self.client.get(url, data=data, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("user", res.data)
        self.assertIn("description", res.data)
        self.assertIn("accept", res.data)

    def test_update_task_successfully(self):
        """Test that updates task information if the task user is the same as the logged on user"""
        data = {
            "name": "Change"
        }
        url = detail_update_task(self.task_1)

        res = self.client.put(url, data=data, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("user", res.data)
        self.assertIn("description", res.data)
        self.assertIn("accept", res.data)

    def test_update_task_unsuccessfully(self):
        """
        test that updates task information if the task user is the same as the logged on user, but in this case
        is unsuccessfully
        """
        data = {
            "name": "Change"
        }
        url = detail_update_task(self.task_3)

        res = self.client.put(url, data=data, format="json")

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual("You do not have permission to perform this action.", res.data["detail"])

    def test_accept_task_successfully(self):
        """Test that you accept a task"""
        self.assertEqual(self.task_1.accept, False)

        data = {
            "accept": True
        }

        url = detail_update_task(self.task_1)

        res = self.client.put(url, data=data, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("user", res.data)
        self.assertIn("description", res.data)
        self.assertIn("accept", res.data)
        self.assertEqual(True, res.data["accept"])

    def test_accepted_task_unsuccessfully(self):
        """Test that you accept a task, but in this case is unsuccessfully"""

        self.assertEqual(self.task_3.accept, False)

        data = {
            "accept": True
        }

        url = detail_update_task(self.task_3)

        res = self.client.put(url, data=data, format="json")

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual("You do not have permission to perform this action.", res.data["detail"])

    def test_delete_task_successfully(self):
        """Test that you delete a task successfully"""

        self.assertEqual(self.task_3.accept, False)

        url = detail_update_task(self.task_2)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_task_unsuccessfully(self):
        """Test that you delete a task, but in this case is unsuccessfully"""

        self.assertEqual(self.task_3.accept, False)

        url = detail_update_task(self.task_4)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual("You do not have permission to perform this action.", res.data["detail"])
