from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'email', 'status', 'phone']
    list_filter = ['user', 'first_name', 'email', 'status']


admin.site.register(Profile, ProfileAdmin)
