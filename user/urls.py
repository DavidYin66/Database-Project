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
]
