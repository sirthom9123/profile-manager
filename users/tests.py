from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Profile


from datetime import datetime, timedelta

# Get 15 years ago date
dated_history = datetime.now() - timedelta(days=15*365) 
history = datetime.strftime(dated_history, '%Y-%m-%d')


class UserTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'test-admin'
        self.password = 'password123'
        self.email = 'emal@test.com'
        self.dob = history
        
    def test_registration(self):
        """ 
        Test case for register user
        """
        username = self.username
        email = self.email
        password = self.password
        user = User(username=username, email=email)
        user.set_password(password)
        user.is_active = True
        user.save()
        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        
    def test_login_user(self):
        """ 
        Test case for login user
        """
        email = self.email
        password = self.password
        username = self.username
        user = User.objects.create_user(email=email, password=password, username=username)
        self.client.login(username=user.username, password=user.password)
        response = self.client.get('/profile/')
        self.assertEqual(user.username, username)
        self.assertTrue(response.status_code, 200)
        
        
    def test_update_user_profile(self):
        """ 
        Test case for update user details and create profile instance
        """
        user = User(email=self.email, username=self.username)
        user.first_name = 'Tester'
        user.last_name = 'Testing'
        user.save()
        self.data = {
            "dob": self.dob,
            "address_line1": '123 Testing street',
            "suburb": 'Wonderboom',
            "city": 'Pretoria',
            "province": 'Gauteng',
            "postal_code": '0002',
            "country": 'South Africa',
            }
        profile = Profile.objects.create(user=user, **self.data)
        self.assertEqual(user, profile.user)
        response = self.client.get('/profile/')
        self.assertTrue(response.status_code, 201)
        
        
    
        

