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
    

class LeaveRequest(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('public', '公假'),
        ('sick', '病假'),
        ('personal', '事假'),
    ]

    STATUS_CHOICES = [
        ('pending', '待审批'),
        ('approved', '已批准'),
        ('rejected', '被驳回'),
    ]

    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(null=True, blank=True)  # 可选的请假理由
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # 默认状态为待审批
    created_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves'
    )

    def __str__(self):
        return f"{self.employee.username} - {self.get_leave_type_display()} ({self.get_status_display()})"
    

class AttendanceSettings(models.Model):
    start_time = models.TimeField()  # 上班时间
    end_time = models.TimeField()    # 下班时间

    def __str__(self):
        return f"上班时间: {self.start_time}, 下班时间: {self.end_time}"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('normal', '正常'),
        ('abnormal', '异常'),
    ]

    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendances')
    check_in_time = models.TimeField(null=True, blank=True)  # 签到时间
    check_out_time = models.TimeField(null=True, blank=True)  # 签退时间
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='normal')  # 正常/异常
    created_at = models.DateField(auto_now_add=True)  # 考勤日期

    class Meta:
        unique_together = ('employee', 'created_at')  # 添加唯一约束

    def __str__(self):
        return f"{self.employee.username} - {self.created_at}"