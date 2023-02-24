from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from .views import authentication_view, profile_view, login_view, register_user

urlpatterns = [
    path('', profile_view, name='profile'),
    path('authentication/', authentication_view, name='authentication'),
    path('login/', login_view, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
]
