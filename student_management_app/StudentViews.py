import datetime
from blog.models import *
from blog.forms import *
from django.views.generic import DeleteView
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.shortcuts import render
from django.urls import reverse,reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .models import *
from django.core.files.storage import FileSystemStorage
from user.models import User

def check_valid_user_access_the_page(request):
    user_type = request.session.get('user_type',-1)
    if user_type != 3:
        raise Http404('method not allowed')
    

def student_home(request):
    if request.user.is_anonymous:
        raise Http404("Anonymous User Hasn't Authorize To Access Students Page")
    elif request.user.user_type == 1:
        raise Http404("Hod Hasn't Authorize To Access Students Page")
    elif request.user.user_type == 2:
        raise Http404("Staffs Hasn't Authorize To Access Students Page")
    elif request.user.user_type == 0:
        raise Http404("Principal Hasn't Authorize To Access student Page")
    
    else:
        print(request.user.id)
        for i in Students.objects.all():
            print(i.admin)
        # student_obj=Students.objects.get(admin=request.user.id)
        user_obj = User.objects.get(id = request.user.id)
        # return HttpResponse("snjs")
        student_obj=Students.objects.get(admin=user_obj)
        attendance_total=AttendanceReport.objects.filter(student_id=student_obj).count()
        attendance_present=AttendanceReport.objects.filter(student_id=student_obj,status=True).count()
        attendance_absent=AttendanceReport.objects.filter(student_id=student_obj,status=False).count()
        dept=Department.objects.get(id=student_obj.dept_id.id)
        subjects=Subjects.objects.filter(dept_id=dept).count()
        subjects_data=Subjects.objects.filter(dept_id=dept)
        session_obj=SessionYearModel.objects.get(id=student_obj.session_year_id.id)

        subject_name=[]
        data_present=[]
        data_absent=[]
        subject_data=Subjects.objects.filter(dept_id=student_obj.dept_id)
        for subject in subject_data:
            attendance=Attendance.objects.filter(subject_id=subject.id)
            attendance_present_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=True,student_id=student_obj.id).count()
            attendance_absent_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=False,student_id=student_obj.id).count()
            subject_name.append(subject.subject_name)
            data_present.append(attendance_present_count)
            data_absent.append(attendance_absent_count)

        post_count = Post.objects.filter(author=request.user.id).count()
        return render(request,"student_template/student_home_template.html",{"post_count":post_count,"total_attendance":attendance_total,"attendance_absent":attendance_absent,"attendance_present":attendance_present,"subjects":subjects,"data_name":subject_name,"data1":data_present,"data2":data_absent})




def student_profile(request):
    check_valid_user_access_the_page(request)
    user=User.objects.get(id=request.user.id)
    student=Students.objects.get(admin=user)
    return render(request,"student_template/student_profile.html",{"user":user,"student":student})

def student_profile_save(request):
    check_valid_user_access_the_page(request)
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_home"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            user=User.objects.get(id=request.user.id)
            user.first_name=first_name
            user.last_name=last_name
            user.save()
            student=Students.objects.get(admin=user)
            student.address=address
            student.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("student_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("student_profile"))


# def student_view_result(request):
#     check_valid_user_access_the_page(request)
#     student=Students.objects.get(admin=request.user.id)
#     studentresult=StudentResult.objects.filter(student_id=student.id)
#     return render(request,"student_template/student_result.html",{"studentresult":studentresult})


def student_view_attendance(request):
    check_valid_user_access_the_page(request)
    student=Students.objects.get(admin=request.user.id)
    dept=student.dept_id
    subjects=Subjects.objects.filter(dept_id=dept)
    return render(request,"student_template/student_view_attendance.html",{"subjects":subjects})

def student_view_attendance_post(request):
    check_valid_user_access_the_page(request)
    subject_id=request.POST.get("subject")
    start_date=request.POST.get("start_date")
    end_date=request.POST.get("end_date")

    start_data_parse=datetime.strptime(start_date,"%Y-%m-%d").date()
    end_data_parse=datetime.strptime(end_date,"%Y-%m-%d").date()
    subject_obj=Subjects.objects.get(id=subject_id)
    user_object=User.objects.get(id=request.user.id)
    stud_obj=Students.objects.get(admin=user_object)

    attendance=Attendance.objects.filter(attendance_date__range=(start_data_parse,end_data_parse),subject_id=subject_obj)
    attendance_reports=AttendanceReport.objects.filter(attendance_id__in=attendance,student_id=stud_obj)
    return render(request,"student_template/student_attendance_data.html",{"attendance_reports":attendance_reports})

def assignment_view(request):
    check_valid_user_access_the_page(request)
    user_obj = User(id=request.user.id)
    session_year = user_obj.student.session_year_id
    subjects = Subjects.objects.filter(session_year=session_year)
    assignment1 = Assignment.objects.filter(subject_id__in=subjects)
    submit_assignment = AssignmentReport.objects.filter(student=user_obj)
    assignment = []
    for ass in assignment1:
        if AssignmentReport.objects.filter(student=user_obj,assignment=ass.id).exists():
            pass
        else:
            assignment.append(ass)
    return render(request,'student_template/assignment_view.html',{'assignments':assignment,'submit_assignments':submit_assignment})
   

def assignment_submit(request,id):
    check_valid_user_access_the_page(request)
    request.session['assignment_id'] = id
    return render(request,'student_template/assignment_submit.html')

def assignment_save(request):
    check_valid_user_access_the_page(request)
    if request.method != 'POST':
        return Http404(request,'method Not Allowed')
    else:
        user = User.objects.get(id=request.user.id)
        assignment_id = request.session['assignment_id']
        assignment_obj = Assignment.objects.get(id=assignment_id)

        if request.FILES.get('assignment_file',False):
            assignment_file=request.FILES['assignment_file']
            fs=FileSystemStorage()
            filename=fs.save(assignment_file.name,assignment_file)
            assignment_file_url=fs.url(filename)
        else:
            assignment_file_url=None
        try:
            assignment_report_obj = AssignmentReport.objects.create(student=user,assignment=assignment_obj,file=assignment_file_url)
            assignment_report_obj.save()
            del request.session['assignment_id']
            messages.success(request,'Assignment Submited Successfully')
            return HttpResponseRedirect(reverse('assignment_view'))
        except Exception as e:
            print(e)
            messages.success(request,'Assignment Not Submited')
            return HttpResponseRedirect(reverse('assignment_submit',kwargs={'id':assignment_id}))
