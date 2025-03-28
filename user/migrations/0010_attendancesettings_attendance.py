# Generated by Django 4.2.16 on 2025-01-01 09:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0009_leaverequest_approved_by"),
    ]

    operations = [
        migrations.CreateModel(
            name="AttendanceSettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name="Attendance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("check_in_time", models.DateTimeField(blank=True, null=True)),
                ("check_out_time", models.DateTimeField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("normal", "正常"), ("abnormal", "异常")],
                        default="normal",
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateField(auto_now_add=True)),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attendances",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
