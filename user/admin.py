from django.contrib import admin
from .models import Profile
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['__str__','return_email', 'timestamp']
    search_fields = ['user', 'bio','location']
    list_filter = ['timestamp']

admin.site.register(Profile,ProfileAdmin)