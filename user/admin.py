from django.contrib import admin
from .models import UserProfile, Employee, LeaveRequest, AttendanceSettings, Attendance

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Employee)
admin.site.register(LeaveRequest)
admin.site.register(AttendanceSettings)
admin.site.register(Attendance)