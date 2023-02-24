from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateTimeField()
    phone_number = models.CharField(max_length=13)
    address_line1 = models.CharField(max_length=255)
    suburb = models.CharField(max_length=255, help_text='Suburb/Town')
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50, help_text='State: Gauteng, Free State, etc...')
    postal_code = models.CharField(max_length=13, blank=True)
    country = models.CharField(max_length=100, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f'Profile for {self.user.first_name}' 
    
    

