from django.contrib import admin
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
import json
from django.dispatch import receiver
from django.db import models
from django.conf import settings

class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None,user_type=0):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.user_type = user_type
        user.save()
        return user

        
    def create_superuser(self, username, email, password=None,user_type=0):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.user_type = user_type
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=255, default="")
    last_name = models.CharField(max_length=255, default="")
    
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_type_data=((0,"Principal"),(1,"HOD"),(2,"Staff"),(3,"Student"))
    user_type=models.IntegerField(default=0,choices=user_type_data)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    @property
    def profilePic(self):
        print(self.user_type,self.hod.profile_pic)
        if self.user_type==0 and self.principal.profile_pic:
            return settings.MEDIA_URL+ str(self.principal.profile_pic)
        if self.user_type==1 and self.hod.profile_pic:
            return settings.MEDIA_URL+ str(self.hod.profile_pic)
        elif self.user_type==2 and self.staff.profile_pic:
            return settings.MEDIA_URL+ str(self.staff.profile_pic)
        elif self.user_type==3 and self.student.profile_pic:
            return settings.MEDIA_URL+str( self.student.profile_pic)
        else:
            return "https://userpic.codeforces.org/no-avatar.jpg"


