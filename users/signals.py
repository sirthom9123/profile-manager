from django.dispatch import receiver
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from .models import UserActivity


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Signal to log signing-in of a users.

    Args:
        sender (User): On sign-in, user instance is logged
        request (get): Get the user obj 
        user (activity): create an instance of the activity.
    """
    if user_logged_in:
        UserActivity.objects.create(user=user, message='{} logged in'.format(user.first_name))
 
 
@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    """Generate failed attempts to the activity model"""
    with open('logs.txt', 'w') as file:
        file.write('Failed authentication by {} at {}'.format(credentials.get('username'),  datetime.now()))
        file.close()
 
 
@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """Signal to log signing-out of a user.

    Args:
        sender (User): On sign-out, user instance is logged
        request (get): Get the user obj 
        user (activity): create an instance of the activity.
    """
    if user_logged_out:
        UserActivity.objects.create(user=user, message='{} logged out'.format(user.first_name))