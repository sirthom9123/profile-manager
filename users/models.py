from django.db import models
from django.contrib.auth.models import User
from .utils import get_coordinates

class UserActivity(models.Model):
    """
    User Activity Model for login/logout activities
    Instance is protected if a user is deleted
    """
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = 'User Activities'

    def __str__(self):
        return str(self.user)
    
    

class Profile(models.Model):
    """
    Model instance extends from default User Model for profile data.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=13)
    address_line1 = models.CharField(max_length=255)
    suburb = models.CharField(max_length=255, help_text='Suburb/Town')
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50, help_text='State: Gauteng, Free State, etc...')
    postal_code = models.CharField(max_length=13, blank=True)
    country = models.CharField(max_length=100, blank=True)
    latitude = models.CharField(max_length=100, blank=True)
    longitude = models.CharField(max_length=100, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f'Profile for {self.user.first_name}' 
    
    """ 
    Get Geocordinates on save with helper function.
    """
    def save(self, *args, **kwargs):
        location = f'{self.address_line1}, {self.suburb}, {self.city}, {self.province}, {self.postal_code}'
        location_coord = get_coordinates(location)
        if self.latitude == "" and self.longitude == "":
            self.latitude = location_coord[1]
            self.longitude = location_coord[0]
        else:
            self.latitude = location_coord[1]
            self.longitude = location_coord[0]
            
        return super().save(*args, **kwargs)

