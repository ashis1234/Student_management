# Generated by Django 3.0.7 on 2021-07-17 08:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0005_auto_20210717_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentreport',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]