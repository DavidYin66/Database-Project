# attendance/urls.py
from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('employee/', views.employee_dashboard, name='employee_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('profile/', views.employee_profile, name='employee_profile'),
    path('admin/employee_list', views.admin_employee_list, name='admin_employee_list'),
    path('admin/edit/<int:employee_id>/', views.admin_edit_employee, name='admin_edit_employee'),
    path('leave/apply/', views.apply_leave, name='apply_leave'),
    path('leave/history/', views.leave_history, name='leave_history'),
    path('admin/manage-leave/', views.manage_leave_requests, name='manage_leave_requests'),
    path('admin/review-leave/<int:leave_id>/<str:action>/', views.review_leave_request, name='review_leave_request'),
    
    # 员工
    path('attendance/', views.employee_attendance, name='employee_attendance'),
    path('attendance/history/', views.attendance_history, name='attendance_history'),

    # 管理员
    path('admin/attendance-settings/', views.manage_attendance_settings, name='manage_attendance_settings'),
    path('admin/manage-attendance/', views.manage_attendance, name='manage_attendance'),
]
