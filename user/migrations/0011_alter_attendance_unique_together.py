# Generated by Django 4.2.16 on 2025-01-01 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0010_attendancesettings_attendance"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="attendance",
            unique_together={("employee", "created_at")},
        ),
    ]
