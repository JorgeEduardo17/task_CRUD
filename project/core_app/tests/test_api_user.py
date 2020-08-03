from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("core_app:create")
TOKEN_URL = reverse("core_app:token")
ME_URL = reverse("core_app:me")


def create_user(**params):
    """Helper function to create new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (Public) """
    def setUp(self):
        self.client = APIClient()
        self.payload = {
            "email": "test@gmail.com",
            "first_name": "Jorge",
            "last_name": "test_last_name",
            "password": "test_pass123",
        }

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        res = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(self.payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_exists(self):
        """Test creating user that already exists fails"""

        create_user(**self.payload)

        res = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """test that password must be more than 5 characters"""
        self.payload["password"] = "pw"
        res = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=self.payload["email"]
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""

        create_user(**self.payload)
        res = self.client.post(TOKEN_URL, self.payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        self.payload["password"] = "wrong"
        res = self.client.post(TOKEN_URL, self.payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn"t exist"""

        res = self.client.post(TOKEN_URL, self.payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {"email": "one", "password": ""})
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email="test@gmail.com",
            first_name="Jorge",
            last_name="test_last_name",
            password="testpass",
        )
        self.client=APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in used"""
        res = self.client.get(ME_URL)

        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
        })

    def test_post_me_not_allowed(self):
        """Test that POST Iis not allowed on the me url"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile fo authenticated user"""
        payload = {"first_name": "new name", "last_name": "new name", "password": "newpassword123"}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, payload["first_name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
