# Generated by Django 3.0.7 on 2021-07-14 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminhod',
            name='address',
            field=models.TextField(default='ban'),
        ),
    ]
