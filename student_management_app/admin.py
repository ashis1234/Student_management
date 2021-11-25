from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin


from .models import *


admin.site.register(Staffs)
admin.site.register(Students)
admin.site.register(HOD)
admin.site.register(Principal)

admin.site.register(SessionYearModel)
admin.site.register(Subjects)
admin.site.register(Department)
admin.site.register(Attendance)
