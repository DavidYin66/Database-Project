# Generated by Django 4.2.16 on 2024-12-14 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0006_alter_employee_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="id",
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
