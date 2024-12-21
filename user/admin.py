from django.contrib import admin
from .models import UserProfile, Employee

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Employee)