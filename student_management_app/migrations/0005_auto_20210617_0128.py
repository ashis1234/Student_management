# Generated by Django 3.0.7 on 2021-06-16 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0004_auto_20210616_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminhod',
            name='profile_pic',
            field=models.ImageField(default='none', upload_to='images'),
        ),
        migrations.AddField(
            model_name='staffs',
            name='profile_pic',
            field=models.ImageField(default='none', upload_to='images'),
        ),
        migrations.AlterField(
            model_name='students',
            name='profile_pic',
            field=models.ImageField(default='none', upload_to='images'),
        ),
    ]
