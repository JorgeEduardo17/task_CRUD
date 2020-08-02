from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelUserProfileTestCase(TestCase):

    def test_create_user_with_email_successful(self):
        """test creating a new user with an email is succesful"""
        email = 'test@gmail.com'
        first_name = 'Jorge'
        last_name = 'test_last_name'
        password = 'test_pass123'
        user = get_user_model().objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@GMAIL.COM'
        user = get_user_model().objects.create_user(email, 'test_first_name', 'test_last_name', 'test123')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '', '', 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@gmail.com',
            'test_first_name',
            'test_last_name',
            'test123'
        )
        self.assertTrue(user.is_admin)
