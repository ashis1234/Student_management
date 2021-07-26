import json
from datetime import datetime
from blog.models import *
from blog.forms import *
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect,Http404
from django.shortcuts import render
from django.urls import reverse,reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView
from .models import *
from django.core.files.storage import FileSystemStorage


def check_valid_user_access_the_page(request):
    user_type = request.session.get('user_type',-1)
    if user_type != '2' and user_type != '1':
        raise Http404('method not allowed')
    



def staff_home(request):
    #For Fetch All Student Under Staff

    if request.user.is_anonymous:
        raise Http404("Anonymous User Hasn't Authorize To Access Teacher Page")
    elif request.user.user_type == '1':
        raise Http404("AdminHod Hasn't Authorize To Access Teacher Page")
    elif request.user.user_type == '3':
        raise Http404("Students Hasn't Authorize To Access Teacher Page")
    elif request.user.user_type == '0':
        raise Http404("Principal Hasn't Authorize To Access teacher Page")
    
    else:
        subjects=Subjects.objects.filter(staff_id=request.user.id)
        
        students_count=Students.objects.filter(dept_id=request.user.staff.dept_id).count()

        #Fetch All Attendance Count
        attendance_count=Attendance.objects.filter(subject_id__in=subjects).count()

        #Fetch All Approve Leave
        user=CustomUser.objects.get(id=request.user.id)
        leave_count=LeaveReport.objects.filter(user=user,leave_status=1).count()
        subject_count=subjects.count()
        post_count = Post.objects.filter(author=request.user.id).count()
        return render(request,"staff_template/staff_home_template.html",{"subject_count":subject_count,"students_count":students_count,"attendance_count":attendance_count,"leave_count":leave_count})





def staff_profile(request):
    check_valid_user_access_the_page(request)
    user=CustomUser.objects.get(id=request.user.id)
    staff=Staffs.objects.get(admin=user)
    return render(request,"staff_template/staff_profile.html",{"user":user,"staff":staff})

def staff_profile_save(request):
    check_valid_user_access_the_page(request)
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()

            staff=Staffs.objects.get(admin=customuser.id)
            staff.address=address
            staff.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("staff_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("staff_profile"))




# /////////////////////////////////////////////////////////////////////////////////////////////

@csrf_exempt
def get_students(request):
    check_valid_user_access_the_page(request)
    subject_id=request.POST.get("subject")
    session_year=request.POST.get("session_year")

    subject=Subjects.objects.get(id=subject_id)
    session_model=SessionYearModel.objects.get(id=session_year)
    students=Students.objects.filter(dept_id=subject.dept_id,session_year_id=session_model)
    list_data=[]
    print(students)

    for student in students:
        name = student.admin.first_name+" "+student.admin.last_name
        if not student.admin.first_name:
            name = student.admin.username
        data_small={"id":student.admin.id,"name": name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)




def staff_take_attendance(request):
    check_valid_user_access_the_page(request)
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_years=SessionYearModel.objects.all()
    return render(request,"staff_template/staff_take_attendance.html",{"subjects":subjects,"session_years":session_years})

@csrf_exempt
def save_attendance_data(request):
    check_valid_user_access_the_page(request)
    student_ids=request.POST.get("student_ids")
    subject_id=request.POST.get("subject_id")
    attendance_date=request.POST.get("attendance_date")
    session_year_id=request.POST.get("session_year_id")

    subject_model=Subjects.objects.get(id=subject_id)
    session_model=SessionYearModel.objects.get(id=session_year_id)
    json_sstudent=json.loads(student_ids)
    #print(data[0]['id'])


    try:
        attendance=Attendance(subject_id=subject_model,attendance_date=attendance_date,session_year_id=session_model)
        attendance.save()

        for stud in json_sstudent:
             student=Students.objects.get(admin=stud['id'])
             attendance_report=AttendanceReport(student_id=student,attendance_id=attendance,status=stud['status'])
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")

def staff_update_attendance(request):
    check_valid_user_access_the_page(request)
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_year_id=SessionYearModel.objects.all()
    return render(request,"staff_template/staff_update_attendance.html",{"subjects":subjects,"session_year_id":session_year_id})

@csrf_exempt
def get_attendance_dates(request):
    check_valid_user_access_the_page(request)
    subject=request.POST.get("subject")
    session_year_id=request.POST.get("session_year_id")
    subject_obj=Subjects.objects.get(id=subject)
    session_year_obj=SessionYearModel.objects.get(id=session_year_id)
    attendance=Attendance.objects.filter(subject_id=subject_obj,session_year_id=session_year_obj)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)

@csrf_exempt
def get_attendance_student(request):
    check_valid_user_access_the_page(request)
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
    list_data=[]


    for student in attendance_data:
        name = student.student_id.admin.first_name+" "+student.student_id.admin.last_name
        if not student.student_id.admin.first_name:
            name = student.student_id.admin.username
        data_small={"id":student.student_id.admin.id,"name":name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

@csrf_exempt
def save_updateattendance_data(request):
    check_valid_user_access_the_page(request)
    student_ids=request.POST.get("student_ids")
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    json_sstudent=json.loads(student_ids)


    try:
        for stud in json_sstudent:
             student=Students.objects.get(admin=stud['id'])
             attendance_report=AttendanceReport.objects.get(student_id=student,attendance_id=attendance)
             attendance_report.status=stud['status']
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")

# ////////////////////////////////////////////////////////////Post//////////////////////////////////////////////////

def Assignment_upload(request):
    check_valid_user_access_the_page(request)
    if request.method != "POST":
        user_id = request.user.id
        subjects = Subjects.objects.filter(staff_id=user_id)
        return render(request,'staff_template/assignment_upload.html',{'subjects' : subjects})
    else:
        subject_id = request.POST.get('subject_id')

    
        if request.FILES.get('assignment',False):
            assignment=request.FILES['assignment']
            fs=FileSystemStorage()
            filename=fs.save(assignment.name,assignment)
            assignment_url=fs.url(filename)
        else:
            assignment_url=None
        if assignment_url == None:
            messages.error(request,'Please add assignment....')
            return HttpResponseRedirect(reverse('assignment_upload'))
        title = request.POST.get('title')
        deadline = request.POST.get('deadline')
        subject_obj = Subjects.objects.get(id=subject_id)
        try:
            assignment = Assignment(title=title,subject_id=subject_obj,deadline=deadline,assignment=assignment_url)
            assignment.save()
            messages.success(request,'Assignment Upload Successfully')
            return HttpResponseRedirect(reverse('assignment_upload'))
        except Exception as e:
            print(e)
            messages.error(request,'assignment not upload')
            return HttpResponseRedirect(reverse('assignment_upload'))
    messages.error(request,'assignment not upload')
    return HttpResponseRedirect(reverse('assignment_upload'))


def assignment_check(request):
    check_valid_user_access_the_page(request)
    user = CustomUser.objects.get(id=request.user.id)
    assignment = []
    subjects = Subjects.objects.filter(staff_id=user)
    for sub in subjects:
        assignment += Assignment.objects.filter(subject_id=sub)
    return render(request,'staff_template/assignment_view.html',{'assignments':assignment,'subjects':subjects})


@csrf_exempt
def get_students_assignment(request):
    check_valid_user_access_the_page(request)
    subject_id = request.POST.get('subject')
    assignment_id = request.POST.get('assignment')
    assignment_obj = Assignment.objects.get(id=assignment_id)
    student_assignment = AssignmentReport.objects.filter(assignment=assignment_obj)
    student_assignment1 = []
    for s_ass in student_assignment:
        name = s_ass.student.first_name+" "+s_ass.student.last_name
        if not s_ass.student.first_name:
            name = s_ass.student.username
        time = str(s_ass.updated_at)
        file = str(s_ass.file)
        data_small={"id":s_ass.student.id,"name": name,'time':time,'file':file}
        student_assignment1.append(data_small)
    return JsonResponse(json.dumps(student_assignment1),content_type="application/json",safe=False)
