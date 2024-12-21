# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Employee

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_employee_profile(sender, instance, created, **kwargs):
    if created:  # 只在新用户创建时执行
        Employee.objects.create(user=instance)  # 自动为每个用户创建一个 Employee 实例

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_employee_profile(sender, instance, **kwargs):
    try:
        instance.employee_profile.save()  # 如果 Employee 已经存在，保存它
    except Employee.DoesNotExist:
        pass
