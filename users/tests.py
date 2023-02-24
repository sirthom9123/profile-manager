from django.test import TestCase
from django.contrib.auth.models import User

class UserTest(TestCase):
    def test_authentication(self):
        username = 'test-admin'
        password = 'password123'
        user = User(username=username)
        user.set_password(password)
        user.save()
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
