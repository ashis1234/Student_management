from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from student_management_app.models import CustomUser

from .models import *
class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser,UserModel)
admin.site.register(Staffs)
admin.site.register(Students)
admin.site.register(AdminHOD)
admin.site.register(Principal)

admin.site.register(SessionYearModel)
admin.site.register(Subjects)
admin.site.register(Department)
admin.site.register(Attendance)
