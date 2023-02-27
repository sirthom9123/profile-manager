from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import folium
from folium.plugins import FastMarkerCluster

from .models import Profile
from .forms import ProfileForm, UserForm

def authentication_view(request):
    """Authentication view
    Args:
        request (get): If a user is authenticated, they will be
        redirected to the home page.

    """
    if request.user.is_authenticated:
        return redirect('/')

    return render(request, 'auth/index.html')


@login_required(login_url='authentication')
def home_view(request):
    """Get the profile data. Iterate and map the data into a map. 
    Args:
        request (get): 
        - queryset: [<Queryset: Profile of Test>, <Queryset: Profile of Test2>]
    Returns:
        html: map to the client side with profile data mapped into it. 
    """
    # Get all the profile data and optimize queryset 
    profile = Profile.objects.select_related('user').all()
    
    # Initialize the map with a center coordinate, for my example I used Pretoria as the center.
    map = folium.Map(location=(-25.7479, 28.2293), zoom_start=8, tiles="OpenStreetMap")
    
    # Iterate through the profiles and map the lat, lon & extra profile data to the marker and Icon.
    for item in profile:
        folium.Marker(location=[item.latitude, item.longitude], popup=f'{item} @ {item.address_line1} {item.city}', icon=folium.Icon(color='red')).add_to(map)
    map_html = map._repr_html_()

        
    context = {
        'map': map_html,
        'profile': profile
    }
    
    return render(request, 'main/index.html', context)


def login_view(request):
    """Handle authenticating users
    
    Args:
        request (post): 
        - Params: email & password 
    
    Conditions: 
        request:
        - Authenticated user is redirected to home page
        - If email does not exists, it will prompt a message
        - If password is incorrect it will prompt a message
        - If params do not match then it will prompt a message
    
    Returns:
        - queryset: Authenticated user
                <Queryset: TestUser>
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
    
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user.is_active:
                login(request, user)
                messages.success(request, f'Welcome {user.first_name} you are now logged in!')
                return redirect('/')
            else:
                messages.error(request, "Credentials do not match, try again!")    

        except:
            messages.error(request, "User with this email does not exist, try signing up!")    
            return redirect('authentication')


def register_user(request):
    """Handle signing up users

    Args:
        request (post): 
        - Params: email, username & password 

    Returns:
        queryset: Created user in the Model & authenticate the user. 
        <Queryset: TestUser>
    """
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
    """Profile view for authenticated user. Only the users data is displayed here.
        The user can create or update their profile with a form generated from django
        forms template.

    Args:
        request (queryset): An exception handles if a profile exists or not. If it 
        does, then a map is generated. 

    Returns:
        context: Users data, Map & forms are rendered to the client side. 
        i.e. context = {'profile': profile, 'map': map, 'form': form}
    """
    user = request.user
    
    try:
        profile = Profile.objects.get(user=user)
        map = folium.Map(location=(profile.latitude, profile.longitude), zoom_start=15, tiles="OpenStreetMap")
        folium.Marker(location=[profile.latitude, profile.longitude], popup=f'{profile.address_line1}', icon=folium.Icon(color='red')).add_to(map)
        map_html = map._repr_html_()
        
    except Profile.DoesNotExist:
        profile = None
        map_html = None
    
    

    # Handle profile form & user form creation and update
    profile_form = ProfileForm(request.POST or None, instance=profile)
    user_form = UserForm(request.POST or None, instance=user)
    if request.method == 'POST':
        if profile_form.is_valid() and user_form.is_valid():
            profile_instance = profile_form.save(commit=False)
            profile_instance.user = user
            profile_instance.save()
            
            user_form.save()

            messages.success(request, 'Profile updated')
            return redirect('profile')
        else:
            messages.error(request, f'{user_form.errors}, {profile_form.errors}')
            return redirect('profile')
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
        'map': map_html,
    }
            
    
    return render(request, 'main/profile.html', context)