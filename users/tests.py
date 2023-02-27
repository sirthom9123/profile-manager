from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Profile

class UserTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'test-admin'
        self.password = 'password123'
        self.email = 'emal@test.com'
        self.request_url = reverse('index')
        
    def test_unauthenticated_user(self):
        """
        Test that an unauthorized user cannot access the map(list) view
        """
        response = self.client.get(self.request_url)
        assert 300 <= response.status_code < 500, "Response.status_code was {}".format(
            response.status_code
        )
        
        
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
        Test case for login user & get all profile data
        """
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/') # Redirect to home page
        self.assertEqual(self.username, self.username)
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
        
        
    
        

