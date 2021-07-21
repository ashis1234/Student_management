from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

# Create your models here.
class SessionYearModel(models.Model):
    id=models.AutoField(primary_key=True)
    session_start_year=models.DateField()
    session_end_year=models.DateField()
    objects=models.Manager()

class CustomUser(AbstractUser):
    user_type_data=((0,"Principal"),(1,"HOD"),(2,"Staff"),(3,"Student"))
    user_type=models.CharField(default=0,choices=user_type_data,max_length=10)
    @property
    def profilePic(self):
        if self.user_type=='0' and self.principal.profile_pic:

            return self.principal.profile_pic
        if self.user_type=='1' and self.hod.profile_pic:
            return self.hod.profile_pic
        elif self.user_type=='2' and self.staff.profile_pic:
            return self.staff.profile_pic
        elif self.user_type=='3' and self.student.profile_pic:
            return self.student.profile_pic
        else:
            return "https://userpic.codeforces.org/no-avatar.jpg"

class Principal(models.Model):
    id=models.AutoField(primary_key=True)
    profile_pic = models.FileField()
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='principal')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Department(models.Model):
    id=models.AutoField(primary_key=True)
    dept_name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    profile_pic = models.FileField()
    dept_id=models.OneToOneField(Department,on_delete=models.CASCADE,related_name='hod_dept')
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='hod')
    address=models.TextField(default="ban")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    @property
    def get_dept_name(self):
        return self.dept_id.dept_name

class Staffs(models.Model):
    id=models.AutoField(primary_key=True)
    profile_pic = models.FileField()
    dept_id=models.ForeignKey(Department,on_delete=models.CASCADE,default=1,related_name='staff_dept')
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name="staff")
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    @property
    def get_dept_name(self):
        return self.dept_id.dept_name




class Subjects(models.Model):
    id=models.AutoField(primary_key=True)
    subject_name=models.CharField(max_length=255)
    dept_id=models.ForeignKey(Department,on_delete=models.CASCADE,default=1)
    staff_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    session_year = models.ForeignKey(SessionYearModel,on_delete=models.CASCADE,default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()



class Students(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='student')
    gender=models.CharField(max_length=255)
    profile_pic = models.FileField()
    address=models.TextField()
    dept_id=models.ForeignKey(Department,on_delete=models.CASCADE,related_name='student_dept')
    session_year_id=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    @property
    def get_dept_name(self):
        return self.dept_id.dept_name


class Assignment(models.Model):
    id=models.AutoField(primary_key=True)
    title = models.CharField(max_length=250)
    subject_id = models.ForeignKey(Subjects,on_delete=models.CASCADE) 
    staff = models.ForeignKey(CustomUser,on_delete=models.CASCADE,default=7)
    upload_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()   
    assignment = models.FileField()
    objects = models.Manager()

    @property
    def check_deadline(self):
        return self.deadline.timestamp() >= timezone.now().timestamp()


class AssignmentReport(models.Model):
    id = models.AutoField(primary_key=True)
    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
    file = models.FileField()
    student = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class LeaveReport(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    leave_date=models.CharField(max_length=255)
    leave_message=models.TextField()
    leave_status=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

  
class FeedBack(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()



class Attendance(models.Model):
    id=models.AutoField(primary_key=True)
    subject_id=models.ForeignKey(Subjects,on_delete=models.DO_NOTHING)
    attendance_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    session_year_id=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class AttendanceReport(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.DO_NOTHING)
    attendance_id=models.ForeignKey(Attendance,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==0:
            Principal.objects.create(admin=instance,profile_pic="")
        elif instance.user_type==1:
            AdminHOD.objects.create(admin=instance,profile_pic="",dept_id=Department.objects.all()[0])
        elif instance.user_type==2:
            Staffs.objects.create(admin=instance,dept_id=Department.objects.all()[0],address="",profile_pic="")
        elif instance.user_type==3:
            Students.objects.create(admin=instance,dept_id=Department.objects.all()[0],session_year_id=SessionYearModel.objects.all()[0],address="",profile_pic="",gender="")


# @receiver(post_save,sender=CustomUser)
# def save_user_profile(sender,instance,**kwargs):
#     if instance.user_type==1:
#         instance.adminhod.save()
#     if instance.user_type==2:
#         instance.staffs.save()
#     if instance.user_type==3:
#         instance.students.save()




