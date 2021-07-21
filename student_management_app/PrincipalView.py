import json
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
import requests
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse,Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from blog.forms import PostForm,EditForm
from .forms import *
from django.db.models import Q
from .models import CustomUser, Staffs, Department, Subjects, Students, SessionYearModel,FeedBack,LeaveReport, Attendance, AttendanceReport
from django.urls import reverse_lazy,reverse
from blog.models import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from students_management_project.settings import ITEM_PER_PAGE


def Pagination_handle(request,obj):
    print("FF")
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

def principal_home(request):
    if request.user.is_anonymous:
        raise Http404("Anonymous User Hasn't Authorize To Access Admin Page")
    elif request.user.user_type == 1:
        raise Http404("Departmental Hod Hasn't Authorize To Access Admin Page")
    elif request.user.user_type == 3:
        raise Http404("Staff Hasn't Authorize To Access Admin Page")
    elif request.user.user_type == 2:
        raise Http404("Students Hasn't Authorize To Access Admin Page")
    else:
        student_count1=Students.objects.all().count()
        staff_count=Staffs.objects.all().count()
        subject_count=Subjects.objects.all().count()
        dept_count=Department.objects.all().count()
        dept_all=Department.objects.all()
        dept_name_list=[]
        subject_count_list=[]
        student_count_list_in_dept=[]
        for dept in dept_all:
            subjects=Subjects.objects.filter(dept_id=dept.id).count()
            students=Students.objects.filter(dept_id=dept.id).count()
            dept_name_list.append(dept.dept_name)
            subject_count_list.append(subjects)
            student_count_list_in_dept.append(students)

        subjects_all=Subjects.objects.all()
        subject_list=[]
        student_count_list_in_subject=[]
        for subject in subjects_all:
            dept=Department.objects.get(id=subject.dept_id.id)
            student_count=Students.objects.filter(dept_id=dept.id).count()
            subject_list.append(subject.subject_name)
            student_count_list_in_subject.append(student_count)

        staffs=Staffs.objects.all()
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
            custom_user = CustomUser.objects.get(id = staff.admin.id)
            leaves=LeaveReport.objects.filter(user=custom_user,leave_status=1).count()
            attendance_present_list_staff.append(attendance)
            attendance_absent_list_staff.append(leaves)
            staff_name_list.append(staff.admin.username)

        # students_all=Students.objects.all()
        # for staff in students_all:
        #     Students.objects.filter(id=staff.id).delete()
        students_all=Students.objects.all()
        attendance_present_list_student=[]
        attendance_absent_list_student=[]
        student_name_list=[]
        for student in students_all:
            attendance=AttendanceReport.objects.filter(student_id=student.id,status=True).count()
            absent=AttendanceReport.objects.filter(student_id=student.id,status=False).count()
            # LeaveReportStudentl
            custom_user = CustomUser.objects.get(id = student.admin.id)
            leaves=LeaveReport.objects.filter(user=custom_user,leave_status=1).count()
            attendance_present_list_student.append(attendance)
            attendance_absent_list_student.append(leaves+absent)
            student_name_list.append(student.admin.username)

        post_count = Post.objects.filter(author=request.user.id).count()
        return render(request,"hod_template/principal_content.html",{"post_count":post_count,"student_count":student_count1,"staff_count":staff_count,"subject_count":subject_count,"course_count":dept_count,"course_name_list":dept_name_list,"subject_count_list":subject_count_list,"student_count_list_in_course":student_count_list_in_dept,"student_count_list_in_subject":student_count_list_in_subject,"subject_list":subject_list,"staff_name_list":staff_name_list,"attendance_present_list_staff":attendance_present_list_staff,"attendance_absent_list_staff":attendance_absent_list_staff,"student_name_list":student_name_list,"attendance_present_list_student":attendance_present_list_student,"attendance_absent_list_student":attendance_absent_list_student})


def add_department(request):
    return render(request,"hod_template/add_course_template.html")

def add_department_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        department=request.POST.get("department")
        try:
            department_model=Department(dept_name=department)
            department_model.save()
            messages.success(request,"Successfully Added Department")
            return HttpResponseRedirect(reverse("add_department"))
        except Exception as e:
            print(e)
            messages.error(request,"Failed To Add Department")
            return HttpResponseRedirect(reverse("add_department"))

def manage_department(request):
    department=Department.objects.all()
    departments = []
    for dept in department:
        departments.append(dept)
    context = {}
    pagination_req,departments = Pagination_handle(request,departments)
    print(pagination_req)
    context['pagination_req'] = pagination_req
    context['departments'] = department
    return render(request,"hod_template/manage_department_template.html",context)

def edit_department(request,dept_id):
    department=Department.objects.get(id=dept_id)
    return render(request,"hod_template/edit_department_template.html",{"department":department,"id":dept_id})

def edit_department_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        dept_id=request.POST.get("dept_id")
        dept_name=request.POST.get("department")

        try:
            department=Department.objects.get(id=dept_id)
            department.dept_name=dept_name
            department.save()
            messages.success(request,"Successfully Edited Department")
            return HttpResponseRedirect(reverse("edit_department",kwargs={"dept_id":dept_id}))
        except:
            messages.error(request,"Failed to Edit Department")
            return HttpResponseRedirect(reverse("edit_department",kwargs={"dept_id":dept_id}))


def manage_staff(request):
    staffs = CustomUser.objects.filter(user_type=1) | CustomUser.objects.filter(user_type=2)
    context = {}
    pagination_req,staffs = Pagination_handle(request,staffs)
    context['pagination_req'] = pagination_req
    context['staffs'] = staffs
    return render(request,"hod_template/manage_staff_template.html",context)

def edit_staff(request,staff_id):
    heading_text = "Staff"
    if request.user.id == staff_id:
        heading_text = "Profile"

    request.session['staff_id']=staff_id

    staff=CustomUser.objects.get(id=staff_id)
    form=EditStaffForm()
    form.fields['email'].initial=staff.email
    form.fields['first_name'].initial=staff.first_name
    form.fields['last_name'].initial=staff.last_name
    form.fields['username'].initial=staff.username
    if staff.user_type=='1':
        hod = AdminHOD.objects.get(admin=staff)
        form.fields['address'].initial=hod.address
    else:
        staff = Staffs.objects.get(admin=staff)
        form.fields['address'].initial = staff.address
    return render(request,"edit_profile.html",{'action_path':'edit_staff_save','id' : staff_id,"form":form,'name' : heading_text})

def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        profile = False
        heading_text = "Staff"
        staff_id=request.session.get("staff_id")
        if request.user.id == staff_id:
            heading_text = "Profile"
            profile = True
        if staff_id==None:
            if profile:
                return HttpResponseRedirect(reverse("staff_home"))
            return HttpResponseRedirect(reverse("manage_staff"))
            

        form=EditStaffForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            
            if request.FILES.get('profile_pic',False):
                profile_pic=request.FILES['profile_pic']
                fs=FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
            else:
                profile_pic_url=None
            try:

                user=CustomUser.objects.get(id=staff_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.save()
                print(user.user_type)
                if user.user_type=='2':
                    staff=Staffs.objects.get(admin=user)
                else:
                    staff = AdminHOD.objects.get(admin=user)
                staff.address=address
                if profile_pic_url!=None:
                    staff.profile_pic=profile_pic_url
                staff.save()
                del request.session['staff_id']
                messages.success(request,"Successfully Edited Staff")
                if profile:
                    return HttpResponseRedirect(reverse("staff_home"))
                return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))
            except Exception as e:
                print(e)
                messages.error(request,"Failed to Edit Staff")
                if profile:
                    return HttpResponseRedirect(reverse("staff_home"))
                return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))
        else:
            form=EditStaffForm(request.POST)
            student=Staffs.objects.get(admin=staff_id)
            return render(request,"edit_profile.html",{'action_path':'edit_staff_save','id' : staff_id,"form":form,'name' : heading_text})

def manage_session(request):
    sessions = SessionYearModel.objects.all()
    context = {}
    pagination_req,sessions = Pagination_handle(request,sessions)
    context['pagination_req'] = pagination_req
    context['sessions'] = sessions
    return render(request,"hod_template/manage_session_template.html",context)

def add_session_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("manage_session"))
    elif 'session_id' in request.POST:
        session_id = request.POST['session_id']
        session = SessionYearModel.objects.get(id=session_id)
        session_start_year = session.session_start_year
        session_end_year = session.session_end_year
        session = SessionYearModel.objects.all()
        return render(request,"hod_template/manage_session_template.html",{'sessions' : session,'session_start_year' : session_start_year,'session_end_year':session_end_year})
    else:
        session_start_year=request.POST.get("session_start")
        session_end_year=request.POST.get("session_end")

        try:
            sessionyear=SessionYearModel(session_start_year=session_start_year,session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Successfully Added Session")
            return HttpResponseRedirect(reverse("manage_session"))
        except:
            messages.error(request, "Failed to Add Session")
            return HttpResponseRedirect(reverse("manage_session"))



# Csrf exempt is a cool feature of django which allows bypassing of csrf verification by django. 
# By default, django check for csrf token with each POST request, it verifies csrf token before rendering the view
@csrf_exempt
def check_email_exist(request):
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

def staff_feedback_message(request):
    feedbacks = []
    for staff in Staffs.objects.all():
        user_obj = CustomUser.objects.get(id = staff.admin.id)
        feedback = FeedBack.objects.filter(user=user_obj)
        feedbacks += feedback

    for hod in AdminHOD.objects.all():
        user_obj = CustomUser.objects.get(id = hod.admin.id)
        feedback = FeedBack.objects.filter(user=user_obj)
        feedbacks += feedback
    context = {}
    pagination_req,feedbacks = Pagination_handle(request,feedbacks)
    context['pagination_req'] = pagination_req
    context['feedbacks'] = feedbacks
    return render(request,"hod_template/staff_feedback_template.html",context)

@csrf_exempt
def staff_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBack.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def staff_leave_view(request):
    #LeaveReport   
    leaves = []
    for staff in Staffs.objects.all():
        user_obj = CustomUser.objects.get(id = staff.admin.id)
        leave=LeaveReport.objects.filter(user=user_obj)
        leaves += leave
    context = {}
    pagination_req,leaves = Pagination_handle(request,leaves)
    context['pagination_req'] = pagination_req
    context['leaves'] = leaves
    return render(request,"hod_template/staff_leave_view.html",context)

def staff_approve_leave(request,leave_id):
    #LeaveReport  
    leave=LeaveReport.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def staff_disapprove_leave(request,leave_id):
    #LeaveReport  
    leave=LeaveReport.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def edit_hod(request,hod_id):
    request.session['hod_id']=hod_id
    hod=Principal.objects.get(admin=hod_id)
    form=EditHODForm()
    form.fields['email'].initial=hod.admin.email
    form.fields['first_name'].initial=hod.admin.first_name
    form.fields['last_name'].initial=hod.admin.last_name
    form.fields['username'].initial=hod.admin.username
    form.fields['profile_pic'].initial = hod.profile_pic
    return render(request,"edit_profile.html",{'action_path':'edit_hod_save','id' : hod_id,"form":form,"hod":hod,'name' : "Profile"})


def edit_hod_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        hod_id=request.session.get("hod_id")
        if hod_id==None:
            return HttpResponseRedirect(reverse("admin_home"))

        form=EditHODForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            try:
                profile_pic=request.FILES['profile_pic']
                fs=FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
            except:
                profile_pic_url=None
            try:
                user=CustomUser.objects.get(id=hod_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.save()

                hod=Principal.objects.get(admin=hod_id)
                if profile_pic_url!=None:
                    hod.profile_pic=profile_pic_url
                hod.save()
                del request.session['hod_id']
                messages.success(request,"Successfully Edited hod")
                return HttpResponseRedirect(reverse("admin_home"))
            except:
                messages.error(request,"Failed to Edit hod")
                return HttpResponseRedirect(reverse("edit_hod",kwargs={"hod_id":hod_id}))
        else:
            form=EditHODForm(request.POST)
            hod=hods.objects.get(admin=hod_id)
            return render(request,"edit_profile.html",{'action_path':'edit_hod_save',"form":form,"id":hod_id,"name":'Profile'})





