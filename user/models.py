from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings

# 定义用户权限的枚举
class UserRole(models.TextChoices):
    EMPLOYEE = 'employee', '员工'
    ADMIN = 'admin', '管理员'

# 扩展 Django 默认的 User 模型
class UserProfile(AbstractUser):
    role = models.CharField(
        max_length=10, 
        choices=UserRole.choices, 
        default=UserRole.EMPLOYEE,
    )

    def __str__(self):
        return self.username


class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    id = models.IntegerField(primary_key=True, editable=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee_profile')
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    contact = models.CharField(max_length=15, null=True, blank=True)  # 电话号码
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # 工资
    position = models.CharField(max_length=100, null=True, blank=True)  # 职位

    def __str__(self):
        return self.name