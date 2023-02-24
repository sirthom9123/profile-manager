from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm, UserForm

def authentication_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    return render(request, 'auth/index.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
    
        try:
            user = User.objects.filter(email=email).first()
            user = authenticate(request, username=user.username, password=password)
            if user.is_active:
                login(request, user)
                messages.success(request, f'Welcome {user.username} you are now logged in!')
                return redirect('profile')
            else:
                messages.error(request, "Credentials do not match, try again!")    

        except:
            messages.error(request, "User with this email does not exit, try signing up!")    
            return redirect('login')


def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                # Check if password has more than 6 characters
                if len(password) < 6:
                    messages.error(request, 'Password length is too short')
                    return redirect('authentication')
                
                # Check if password matches
                if password != password2:
                    messages.error(request, 'Password does not match')
                    return redirect('authentication')
            
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = True
                user.save()
                user = authenticate(request, username=user.username, password=password)
                
                if user:
                    login(request, user)
                    messages.success(request, f'Account created successfully. Welcome {user.username} you are now logged in!')
                    return redirect('profile')
            
            else:
                messages.error(request, 'Email already exists')
                return redirect('authentication')
        else:
            messages.error(request, 'Account with username already exists')
            return redirect('authentication')
            
            
            

@login_required(login_url='authentication')
def profile_view(request):
    
    return render(request, 'main/profile.html')