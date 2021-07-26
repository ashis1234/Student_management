import datetime
import json
import os
from .forms import *
from blog.models import *
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.shortcuts import render
from django.urls import reverse

from student_management_app.EmailBackEnd import EmailBackEnd
from .models import *
from django.conf import settings


from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
# from .serializers import *


# class SessionYearModelViewSet(viewsets.ModelViewSet):
#     queryset = SessionYearModel.objects.all()
#     serializer_class = SessionYearModelSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class CustomUSerViewSet(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class StaffsViewSet(viewsets.ModelViewSet):
#     queryset = Staffs.objects.all()
#     serializer_class = StaffsSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class StudentsViewSet(viewsets.ModelViewSet):
#     queryset = Students.objects.all()
#     serializer_class = StudentsSerializer
#     permission_classes = [permissions.IsAuthenticated]



# class SubjectsViewSet(viewsets.ModelViewSet):
#     queryset = Subjects.objects.all()
#     serializer_class = SubjectsSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class CoursesViewSet(viewsets.ModelViewSet):
#     queryset = Courses.objects.all()
#     serializer_class = CoursesSerializer
#     permission_classes = [permissions.IsAuthenticated]





def ShowLoginPage(request):
    if not request.user.is_anonymous: 
        raise Http404("method not allowed")
    return render(request,"login_page.html")

def doLogin(request):
    if request.method!="POST":
        raise Http404("method not allowed")
    else:
        LoginFrom = request.session.get('login-from')
        subpath = request.session.get('subpath')
        ItemId = request.session.get('item-id')
        if LoginFrom:
            del request.session['login-from']
        if subpath:
            del request.session['subpath']
            del request.session['item-id']


        # captcha_token=request.POST.get("g-recaptcha-response")
        # cap_url="https://www.google.com/recaptcha/api/siteverify"
        # cap_secret="6LeWtqUZAAAAANlv3se4uw5WAg-p0X61CJjHPxKT"
        # cap_data={"secret":cap_secret,"response":captcha_token}
        # cap_server_response=requests.post(url=cap_url,data=cap_data)
        # cap_json=json.loads(cap_server_response.text)

        # if cap_json['success']==False:
        #     messages.error(request,"Invalid Captcha Try Again")
        #     return HttpResponseRedirect("/")
        # print(request.POST.get("username"),request.POST.get("password"))
        user=EmailBackEnd.authenticate(request,username=request.POST.get("username"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            request.session['user_type'] = user.user_type
            if subpath:
                return HttpResponseRedirect(reverse(LoginFrom,kwargs={subpath:ItemId}))
            if LoginFrom:
                return HttpResponseRedirect(reverse(LoginFrom))
            
            if user.user_type=='0':
                return HttpResponseRedirect('principal_home')
            elif user.user_type=="1":
                return HttpResponseRedirect('admin_home')
            elif user.user_type=="2":
                return HttpResponseRedirect("staff_home")
            else:
                return HttpResponseRedirect("student_home")

        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect(reverse("show_login"))


def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User : "+request.user.email+" usertype : "+str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    if request.session.get('user_type'):
        del request.session['user_type']
    LoginFrom = request.session.get('login-from')
    subpath = request.session.get('subpath')
    ItemId = request.session.get('item-id')
    if LoginFrom:
        del request.session['login-from']
    if subpath:
        del request.session['subpath']
        del request.session['item-id']

    if subpath:
        return HttpResponseRedirect(reverse(LoginFrom,kwargs={subpath:ItemId}))
    if LoginFrom:
        return HttpResponseRedirect(reverse(LoginFrom))
            
    return HttpResponseRedirect(reverse("home"))


def Testurl(request):
    return HttpResponse("Ok")

def signup_admin(request):
    if not request.user.is_anonymous:
        raise Http404('method not allowed')
    department = Department.objects.all()
    return render(request,"signup.html",{'name':'Hod','departments':department,'action_path':'do_hod_signup'})

def signup_principal(request):
    if not request.user.is_anonymous:
        raise Http404('method not allowed')
    return render(request,"signup.html",{'name':'Principal','action_path':'do_principal_signup'})

def signup_student(request):
    if not request.user.is_anonymous:
        raise Http404('method not allowed')
    department = Department.objects.all()
    session_year = SessionYearModel.objects.all()
    return render(request,"signup.html",{'name':'Student','departments':department,'session_years':session_year,'action_path':'do_signup_student'})

def signup_staff(request):
    if not request.user.is_anonymous:
        raise Http404('method not allowed')
    department = Department.objects.all()

    return render(request,"signup.html",{'name':'Staff','departments':department,'action_path':'do_staff_signup'})


def check_email_username(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        messages.error(request,'Username already exists')
        return True
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        messages.error(request,'Email already exists')
        return True
    return False

def do_principal_signup(request):
    if request.method != 'POST':
        raise Http404('method not allowed')
    if check_email_username(request):
        return HttpResponseRedirect(reverse('show_login'))
    
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")
    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=0)
        user.save()
        messages.success(request,"Successfully Created Admin")
        return HttpResponseRedirect(reverse("show_login"))
    except Exception as e:
        # messages.error(request,"Failed to Create Admin")
        return HttpResponseRedirect(reverse("show_login"))

def do_hod_signup(request):
    if request.method != 'POST':
        raise Http404('method not allowed')
    if check_email_username(request):
        return HttpResponseRedirect(reverse('show_login'))
    
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")
    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=1)
        user.save()
        print(user.user_type)
        messages.success(request,"Successfully Created Admin")
        return HttpResponseRedirect(reverse("show_login"))
    except Exception as e:
        print(e)
        # messages.error(request,"Failed to Create Admin")
        return HttpResponseRedirect(reverse("show_login"))

def do_staff_signup(request):
    if request.method != 'POST':
        raise Http404('method not allowed')
    if check_email_username(request):
        return HttpResponseRedirect(reverse('show_login'))
    
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")
    address=request.POST.get("address")
    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=2)
        user.staffs.address=address
        user.save()
        messages.success(request,"Successfully Created Staff")
        return HttpResponseRedirect(reverse("show_login"))
    except Exception as e:
        print()
        print(e)
        print()
        # messages.error(request,"Failed to Create Staff")
        return HttpResponseRedirect(reverse("show_login"))

def do_signup_student(request):
    if request.method != 'POST':
        raise Http404('method not allowed')
    if check_email_username(request):
        return HttpResponseRedirect(reverse('show_login'))
    
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")
    address=request.POST.get("address")
    department=request.POST.get("department")
    session_year=request.POST.get("session_year")
    dept_id = Department.objects.get(dept_name = department)
    session_year_id = SessionYearModel.objects.get(id=session_year)

    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=3)
        user.student.address = address
        user.student.dept_id = dept_id
        user.student.session_year_id = session_year_id
        user.save()
        messages.success(request,"Successfully Created Student")
        return HttpResponseRedirect(reverse("show_login"))
    except Exception as e:
        # messages.error(request,"Failed to Create Student")
        return HttpResponseRedirect(reverse("show_login"))


def apply_leave(request):
    user_type = request.session.get('user_type',-1)
    if user_type not in ['0','1','2']:
        raise Http404('method not allowed')
    user_obj = CustomUser.objects.get(id=request.user.id)
    leave_data=LeaveReport.objects.filter(user=user_obj)
    return render(request,"leave.html",{"leave_data":leave_data})


def apply_leave_save(request):
    user_type = request.session.get('user_type',-1)
    if user_type not in ['0','1','2']:
        raise Http404('method not allowed')
    if request.method!="POST":
        return HttpResponseRedirect(reverse("apply_leave"))
    else:
        leave_date=request.POST.get("leave_date")
        leave_msg=request.POST.get("leave_msg")
        user_obj = CustomUser.objects.get(id=request.user.id)
        try:
            leave_report=LeaveReport(user=user_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("apply_leave"))
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("apply_leave"))



def feedback(request):
    user_type = request.session.get('user_type',-1)
    if user_type not in ['0','1','2']:
        raise Http404('method not allowed')
    user_obj = CustomUser.objects.get(id=request.user.id)
    feedback_data=FeedBack.objects.filter(user=user_obj)
    return render(request,"feedback.html",{"feedback_data":feedback_data})

def feedback_save(request):
    user_type = request.session.get('user_type',-1)
    if user_type not in ['0','1','2']:
        raise Http404('method not allowed')
    if request.method!="POST":
        return HttpResponseRedirect(reverse("feedback_save"))
    else:
        feedback_msg=request.POST.get("feedback_msg")
        user_obj = CustomUser.objects.get(id=request.user.id)
        try:
            feedback=FeedBack(user=user_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("feedback"))


def Delete(request,type,id):
    if request.user.is_anonymous:
        raise Http404('method not allowed')
    if request.method!="POST":
        return render(request,'delete_post.html',{'name':type,'id' : id})
    else:
        if 'yes' in request.POST:
            try:
                if type == "post":
                    Post.objects.filter(id=id).delete()
                    messages.success(request,type.capitalize() + ' Deleted Successfully')
                elif type == "student":
                    student = Students.objects.get(id=id)
                    CustomUser.objects.filter(id=student.admin.id).delete()
                    messages.success(request,type.capitalize() + ' Deleted Successfully')
                elif type == 'staff':
                    user = CustomUser.objects,get(id=id)
                    if user.user_type == '1':
                        staff = AdminHOD.objects.get(admin=user)
                    else:
                        staff = Staffs.objects.get(admin=user)
                    
                    user.delete()
                    staff.delete()
                    messages.success(request,type.capitalize() + ' Deleted Successfully')
                elif type == 'department':
                    Department.objects.filter(id=id).delete()
                    messages.success(request,type.capitalize() + ' Deleted Successfully')
                elif type=='subject':
                    Subjects.objects.filter(id=id).delete()
                    messages.success(request,type.capitalize() + ' Deleted Successfully')
                elif type=='session':
                    SessionYearModel.objects.filter(id=id).delete()
                    messages.success(request,type.capitalize() + ' Deleted Successfully')
                elif type=='category':
                    cat_obj = Category.objects.get(id=id)
                    post_cat = Post_category.objects.filter(cat_id = cat_obj)
                    print(cat_obj,post_cat)
                    for p_cat in post_cat:
                        post = p_cat.post_id
                        post.category.remove(cat_obj.name)
                        post.save()
                        p_cat.delete()
                    cat_obj.delete()
                    messages.success(request,type.capitalize() + ' Deleted Successfully')       
            except Exception as e:
                messages.error(request,type.capitalize() + ' Not Deleted')
        else:
            messages.error(request,type.capitalize() + ' Not Deleted')
        return HttpResponseRedirect(reverse("manage_"+type))



    

def ProfileView(request,user):
    try:
        user = CustomUser.objects.get(username=user)
    except Exception as e:
        return HttpResponse("user Not Exist")
    return HttpResponse("user Exist")