from django.dispatch import receiver
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from .models import UserActivity


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    if user_logged_in:
        UserActivity.objects.create(user=user, message='{} logged in'.format(user.first_name))
 
 
@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    print('Failed authentication by {} at {}'.format(credentials.get('username'),  datetime.now()))
 
 
@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    if user_logged_out:
        UserActivity.objects.create(user=user, message='{} logged out'.format(user.first_name))