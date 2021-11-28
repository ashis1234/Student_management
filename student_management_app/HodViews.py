import json
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
import requests
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse,Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from blog.forms import PostForm,EditForm
from .forms import *
from .models import  Staffs, Department, Subjects, Students, SessionYearModel,FeedBack,LeaveReport, Attendance, AttendanceReport
from django.urls import reverse_lazy,reverse
from blog.models import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from students_management_project.settings import ITEM_PER_PAGE
from user.models import User


def check_valid_user_access_the_page(request):
    user_type = request.session.get('user_type',-1)
    if user_type != 1:
        raise Http404('method not allowed')
    


def Pagination_handle(request,obj):
    pagination_req = len(obj) > ITEM_PER_PAGE
    page = request.GET.get('page', 1)
    obj_paginator = Paginator(obj, ITEM_PER_PAGE)
    try:
        obj = obj_paginator.page(page)
    except PageNotAnInteger:
        obj = obj_paginator.page(ITEM_PER_PAGE)
    except EmptyPage:
        obj = obj_paginator.page(obj_paginator.num_pages)
    return pagination_req,obj

def Hod_home(request):
    print(request.user.user_type)
    if request.user.is_anonymous:
        raise Http404("Anonymous User Hasn't Authorize To Access Admin Page")
    elif request.user.user_type == 3:
        raise Http404("Staff Hasn't Authorize To Access Admin Page")
    elif request.user.user_type == 2:
        raise Http404("Students Hasn't Authorize To Access Admin Page")
    elif request.user.user_type == 0:
        raise Http404("Principal Hasn't Authorize To Access Admin Page")
    else:
        dept_id = request.user.hod.dept_id
        student_count1=Students.objects.filter(dept_id=dept_id).count()
        staff_count=Staffs.objects.filter(dept_id=dept_id).count()
        subject_count=Subjects.objects.filter(dept_id=dept_id).count()
        
        subjects = Subjects.objects.filter(dept_id=dept_id)
        subject_list = []
        student_count_list_in_subject = []
        for sub in subjects:
            subject_list.append(sub.subject_name)
            count = Students.objects.filter(session_year_id=sub.session_year).count()
            student_count_list_in_subject.append(count)

        staffs=Staffs.objects.filter(dept_id=dept_id)
        # for staff in staffs:
        #     Staffs.objects.filter(id=staff.id).delete()
        # staffs=Staffs.objects.all()
        attendance_present_list_staff=[]
        attendance_absent_list_staff=[]
        staff_name_list=[]
        for staff in staffs:
            subject_ids=Subjects.objects.filter(staff_id=staff.admin.id)
            attendance=Attendance.objects.filter(subject_id__in=subject_ids).count()
        #LeaveReport       
            custom_user = User.objects.get(id = staff.admin.id)
            leaves=LeaveReport.objects.filter(user=custom_user,leave_status=1).count()
            attendance_present_list_staff.append(attendance)
            attendance_absent_list_staff.append(leaves)
            staff_name_list.append(staff.admin.username)

        # students_all=Students.objects.all()
        # for staff in students_all:
        #     Students.objects.filter(id=staff.id).delete()
        students_all=Students.objects.filter(dept_id=dept_id)
        attendance_present_list_student=[]
        attendance_absent_list_student=[]
        student_name_list=[]
        for student in students_all:
            attendance=AttendanceReport.objects.filter(student_id=student.id,status=True).count()
            absent=AttendanceReport.objects.filter(student_id=student.id,status=False).count()
            # LeaveReportStudentl
            custom_user = User.objects.get(id = student.admin.id)
            leaves=LeaveReport.objects.filter(user=custom_user,leave_status=1).count()
            attendance_present_list_student.append(attendance)
            attendance_absent_list_student.append(leaves+absent)
            student_name_list.append(student.admin.username)

        post_count = Post.objects.filter(author=request.user.id).count()
        return render(request,"hod_template/home_content.html",{"post_count":post_count,"student_count":student_count1,"staff_count":staff_count,"subject_count":subject_count,"student_count_list_in_subject":student_count_list_in_subject,"subject_list":subject_list,"staff_name_list":staff_name_list,"attendance_present_list_staff":attendance_present_list_staff,"attendance_absent_list_staff":attendance_absent_list_staff,"student_name_list":student_name_list,"attendance_present_list_student":attendance_present_list_student,"attendance_absent_list_student":attendance_absent_list_student})


# def add_staff(request):
#     return render(request,"hod_template/add_staff_template.html")

# def add_staff_save(request):
#     if request.method!="POST":
#         return HttpResponse("Method Not Allowed")
#     else:
#         first_name=request.POST.get("first_name")
#         last_name=request.POST.get("last_name")
#         username=request.POST.get("username")
#         email=request.POST.get("email")
#         password=request.POST.get("password")
#         address=request.POST.get("address")
#         try:
#             user=User.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
#             user.staff.address=address
#             user.save()
#             messages.success(request,"Successfully Added Staff")
#             return HttpResponseRedirect(reverse("add_staff"))
#         except:
#             messages.error(request,"Failed to Add Staff")
#             return HttpResponseRedirect(reverse("add_staff"))

# def add_student(request):
#     return render(request,"hod_template/add_student_template.html")

# def add_student_save(request):
#     if request.method!="POST":
#         return HttpResponse("Method Not Allowed")
#     else:
#         first_name=request.POST.get("first_name")
#         last_name=request.POST.get("last_name")
#         username=request.POST.get("username")
#         email=request.POST.get("email")
#         password=request.POST.get("password")
#         address=request.POST.get("address")
#         try:
#             user=User.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
#             user.student.address=address
#             user.save()
#             messages.success(request,"Successfully Added Student")
#             return HttpResponseRedirect(reverse("add_student"))
#         except:
#             messages.error(request,"Failed to Add Student")
#             return HttpResponseRedirect(reverse("add_student"))



def add_subject(request):
    check_valid_user_access_the_page(request)
    departments=Department.objects.all()
    session_year=SessionYearModel.objects.all()
    staffs=User.objects.filter(user_type=2) | User.objects.filter(user_type=1)
    return render(request,"hod_template/add_subject_template.html",{"staffs":staffs,"departments":departments,'session_years':session_year})

def add_subject_save(request):
    check_valid_user_access_the_page(request)
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_name=request.POST.get("subject_name")
        session_id = request.POST.get('session')
        department = request.user.hod.dept_id
        staff_id=request.POST.get("staff")
        staff=User.objects.get(id=staff_id)
        session_year_id = SessionYearModel.objects.get(id=session_id)
        try:
            subject=Subjects(subject_name=subject_name,dept_id=department,staff_id=staff,session_year=session_year_id)
            subject.save()
            messages.success(request,"Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request,"Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_subject"))



def manage_student(request):
    check_valid_user_access_the_page(request)
    students=Students.objects.all()
    context = {}
    pagination_req,students = Pagination_handle(request,students)
    context['pagination_req'] = pagination_req
    context['students'] = students
    return render(request,"hod_template/manage_student_template.html",context)



def manage_subject(request):
    check_valid_user_access_the_page(request)
    subjects=Subjects.objects.all()
    context = {}
    pagination_req,subjects = Pagination_handle(request,subjects)
    context['pagination_req'] = pagination_req
    context['subjects'] = subjects
    return render(request,"hod_template/manage_subject_template.html",context)




def edit_student(request,student_id):
    check_valid_user_access_the_page(request)
    heading_text = "Student"
    if request.user.id == student_id:
        heading_text = "Profile"
    request.session['student_id']=student_id
    student=Students.objects.get(admin=student_id)
    form=EditStudentForm()
    form.fields['email'].initial=student.admin.email
    form.fields['first_name'].initial=student.admin.first_name
    form.fields['last_name'].initial=student.admin.last_name
    form.fields['username'].initial=student.admin.username
    form.fields['address'].initial=student.address
    form.fields['course'].initial=student.dept_id.id
    form.fields['sex'].initial=student.gender
    form.fields['session_year'].initial=student.session_year_id
    return render(request,"edit_profile.html",{'action_path':'edit_student_save','id' : student_id,"form":form,"student":student,'name' : heading_text})

def edit_student_save(request):
    check_valid_user_access_the_page(request)
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        profile = False
        student_id=request.session.get("student_id")
        heading_text = "Student"
        if request.user.id == student_id:
            heading_text = "Profile"
            profile = True
        if student_id==None:
            if profile:
                return HttpResponseRedirect(reverse("student_home"))
            return HttpResponseRedirect(reverse("manage_student"))
        
        form=EditStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            session_year_id = form.cleaned_data["session_year"]
            course_id = form.cleaned_data["course"]
            sex = form.cleaned_data["sex"]

            if request.FILES.get('profile_pic',False):
                profile_pic=request.FILES['profile_pic']
                fs=FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
            else:
                profile_pic_url=None
            try:
                user=User.objects.get(id=student_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.save()

                student=Students.objects.get(admin=student_id)
                student.address=address
                session_year = SessionYearModel.objects.get(id=session_year_id)
                student.session_year_id=session_year
                student.gender=sex
                course=Department.objects.get(id=course_id)
                student.dept_id=course
                if profile_pic_url!=None:
                    student.profile_pic=profile_pic_url
                student.save()
                del request.session['student_id']
                messages.success(request,"Successfully Edited Student")
                if profile:
                    return HttpResponseRedirect(reverse("student_home"))
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
            except:
                messages.error(request,"Failed to Edit Student")
                if profile:
                    return HttpResponseRedirect(reverse("student_home"))
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
        else:
            form=EditStudentForm(request.POST)
            student=Students.objects.get(admin=student_id)
            return render(request,"edit_profile.html",{'action_path':'edit_student_save',"form":form,"id":student_id,"name":heading_text})



def edit_subject(request,subject_id):
    check_valid_user_access_the_page(request)
    subject=Subjects.objects.get(id=subject_id)
    departments=Department.objects.all()
    staffs=User.objects.filter(user_type=2) | User.objects.filter(user_type=1)
    session_years = SessionYearModel.objects.all() 
    return render(request,"hod_template/edit_subject_template.html",{"subject":subject,"staffs":staffs,"departments":departments,"id":subject_id,'session_years':session_years})

def edit_subject_save(request):
    check_valid_user_access_the_page(request)
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id=request.POST.get("subject_id")
        subject_name=request.POST.get("subject_name")
        staff_id=request.POST.get("staff")
        session_year = request.POST.get('session')
        dept_id=request.POST.get("department")

        try:
            subject=Subjects.objects.get(id=subject_id)
            subject.subject_name=subject_name
            staff=User.objects.get(id=staff_id)
            subject.staff_id=staff
            session_year_id = SessionYearModel.objects.get(id=session_year)
            department=Department.objects.get(id=dept_id)
            subject.dept_id=department
            subject.session_year_id = session_year_id
            subject.save()

            messages.success(request,"Successfully Edited Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))
        except:
            messages.error(request,"Failed to Edit Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))






def student_feedback_message(request):
    check_valid_user_access_the_page(request)
    feedbacks = []
    for student in Students.objects.all():
        user_obj = User.objects.get(id = student.admin.id)
        feedback =FeedBack.objects.filter(user=user_obj)
        feedbacks += feedback
    context = {}
    pagination_req,feedbacks = Pagination_handle(request,feedbacks)
    context['pagination_req'] = pagination_req
    context['feedbacks'] = feedbacks
    return render(request,"hod_template/student_feedback_template.html",context)

@csrf_exempt
def student_feedback_message_replied(request):
    check_valid_user_access_the_page(request)
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBack.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def student_leave_view(request):
    check_valid_user_access_the_page(request)
    # LeaveReportStudentl
    leaves = []
    for student in Students.objects.all():
        user_obj = User.objects.get(id = student.admin.id)
        leave=LeaveReport.objects.filter(user=user_obj)
        leaves += leave
    context = {}
    pagination_req,leaves = Pagination_handle(request,leaves)
    context['pagination_req'] = pagination_req
    context['leaves'] = leaves
    return render(request,"hod_template/student_leave_view.html",context)

def student_approve_leave(request,leave_id):
    check_valid_user_access_the_page(request)
    # LeaveReportStudent
    leave=LeaveReport.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))

def student_disapprove_leave(request,leave_id):
    check_valid_user_access_the_page(request)
    # LeaveReportStudent
    leave=LeaveReport.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def admin_view_attendance(request):
    check_valid_user_access_the_page(request)
    subjects=Subjects.objects.all()
    session_year_id=SessionYearModel.objects.all()
    return render(request,"hod_template/admin_view_attendance.html",{"subjects":subjects,"session_year_id":session_year_id})

@csrf_exempt
def admin_get_attendance_dates(request):
    check_valid_user_access_the_page(request)
    subject=request.POST.get("subject")
    session_year_id=request.POST.get("session_year_id")
    subject_obj=Subjects.objects.get(id=subject)
    session_year_obj=SessionYearModel.object.get(id=session_year_id)
    attendance=Attendance.objects.filter(subject_id=subject_obj,session_year_id=session_year_obj)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)


@csrf_exempt
def admin_get_attendance_student(request):
    check_valid_user_access_the_page(request)
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)



