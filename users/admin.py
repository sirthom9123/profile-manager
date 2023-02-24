from django.contrib import admin

from .models import Profile, UserActivity

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'phone_number', 'suburb', 'province', 'created_date', 'updated_date']
    list_filter = ['id', 'user', 'suburb', 'created_date']
    search_fields = ['user__first_name', 'user__last_name', 'suburb']
    
    
    
@admin.register(UserActivity)
class UserActivitiesAdmin(admin.ModelAdmin):
    list_display = ('user', 'created')
    list_filter = ('user', 'created')
    search_fields = ('user',)