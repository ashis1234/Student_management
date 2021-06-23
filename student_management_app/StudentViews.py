import datetime
from blog.models import *
from blog.forms import *
from django.views.generic import DeleteView
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse,reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from .models import Students, Courses, Subjects, CustomUser, Attendance, AttendanceReport,LeaveReportStudent, FeedBackStudent, StudentResult, SessionYearModel


def student_home(request):
    student_obj=Students.objects.get(admin=request.user.id)
    attendance_total=AttendanceReport.objects.filter(student_id=student_obj).count()
    attendance_present=AttendanceReport.objects.filter(student_id=student_obj,status=True).count()
    attendance_absent=AttendanceReport.objects.filter(student_id=student_obj,status=False).count()
    course=Courses.objects.get(id=student_obj.course_id.id)
    subjects=Subjects.objects.filter(course_id=course).count()
    subjects_data=Subjects.objects.filter(course_id=course)
    session_obj=SessionYearModel.object.get(id=student_obj.session_year_id.id)
    class_room=OnlineClassRoom.objects.filter(subject__in=subjects_data,is_active=True,session_years=session_obj)

    subject_name=[]
    data_present=[]
    data_absent=[]
    subject_data=Subjects.objects.filter(course_id=student_obj.course_id)
    for subject in subject_data:
        attendance=Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=True,student_id=student_obj.id).count()
        attendance_absent_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=False,student_id=student_obj.id).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)

    return render(request,"student_template/student_home_template.html",{"total_attendance":attendance_total,"attendance_absent":attendance_absent,"attendance_present":attendance_present,"subjects":subjects,"data_name":subject_name,"data1":data_present,"data2":data_absent,"class_room":class_room})



def student_view_attendance(request):
    student=Students.objects.get(admin=request.user.id)
    course=student.course_id
    subjects=Subjects.objects.filter(course_id=course)
    return render(request,"student_template/student_view_attendance.html",{"subjects":subjects})

def student_view_attendance_post(request):
    subject_id=request.POST.get("subject")
    start_date=request.POST.get("start_date")
    end_date=request.POST.get("end_date")

    start_data_parse=datetime.datetime.strptime(start_date,"%Y-%m-%d").date()
    end_data_parse=datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
    subject_obj=Subjects.objects.get(id=subject_id)
    user_object=CustomUser.objects.get(id=request.user.id)
    stud_obj=Students.objects.get(admin=user_object)

    attendance=Attendance.objects.filter(attendance_date__range=(start_data_parse,end_data_parse),subject_id=subject_obj)
    attendance_reports=AttendanceReport.objects.filter(attendance_id__in=attendance,student_id=stud_obj)
    return render(request,"student_template/student_attendance_data.html",{"attendance_reports":attendance_reports})

def student_apply_leave(request):
    staff_obj = Students.objects.get(admin=request.user.id)
    leave_data=LeaveReportStudent.objects.filter(student_id=staff_obj)
    return render(request,"student_template/student_apply_leave.html",{"leave_data":leave_data})

def student_apply_leave_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_apply_leave"))
    else:
        leave_date=request.POST.get("leave_date")
        leave_msg=request.POST.get("leave_msg")

        student_obj=Students.objects.get(admin=request.user.id)
        try:
            leave_report=LeaveReportStudent(student_id=student_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))


def student_feedback(request):
    staff_id=Students.objects.get(admin=request.user.id)
    feedback_data=FeedBackStudent.objects.filter(student_id=staff_id)
    return render(request,"student_template/student_feedback.html",{"feedback_data":feedback_data})

def student_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_feedback"))
    else:
        feedback_msg=request.POST.get("feedback_msg")

        student_obj=Students.objects.get(admin=request.user.id)
        try:
            feedback=FeedBackStudent(student_id=student_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))

def student_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    student=Students.objects.get(admin=user)
    return render(request,"student_template/student_profile.html",{"user":user,"student":student})

def student_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()

            student=Students.objects.get(admin=customuser)
            student.address=address
            student.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("student_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("student_profile"))


def student_view_result(request):
    student=Students.objects.get(admin=request.user.id)
    studentresult=StudentResult.objects.filter(student_id=student.id)
    return render(request,"student_template/student_result.html",{"studentresult":studentresult})



# ///////////////////////////////////////


def add_post(request):
    form = PostForm()
    if request.method != 'POST':
        return render(request,'student_template/add_post.html',{'form' : form})
    else:
        form = PostForm(request.POST)
        if form.is_valid():
            user_id = request.user.id
            title = form.cleaned_data['title']
            title_tag = form.cleaned_data['title_tag']
            body = form.cleaned_data['body']
            category = form.cleaned_data['category']
            user = CustomUser.objects.get(id=user_id)
            try:
                post = Post(title=title,title_tag=title_tag,body=body,author=user,category=category)
                post.save()
                messages.success(request,"Successfully Added Post")
            except:
                messages.error(request,"Failed to added Post")
            return HttpResponseRedirect(reverse("add_post_for_students"))

def edit_post(request,post_id):
    request.session['post_id']=post_id
    post=Post.objects.get(id=post_id)
    form=EditForm()
    form.fields['title'].initial=post.title
    form.fields['title_tag'].initial=post.title_tag
    form.fields['body'].initial=post.body
    form.fields['category'].initial=post.category
    return render(request,"student_template/edit_post.html",{"form":form,"id":post_id})

def edit_post_save(request):
    form = EditForm()
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        post_id=request.session.get("post_id")
        if post_id==None:
            return HttpResponseRedirect(reverse("manage_post_for_students"))

        form = EditForm(request.POST)
        if form.is_valid():
            user_id = request.user.id
            title = form.cleaned_data['title']
            title_tag = form.cleaned_data['title_tag']
            body = form.cleaned_data['body']
            category = form.cleaned_data['category']
            user = CustomUser.objects.get(id=user_id)
            try:
                post = Post.objects.get(id=post_id)
                post.title = title
                post.title_tag = title_tag
                post.body = body
                post.category = category
                post.save()
                del request.session['post_id']
                messages.success(request,"Successfully post edited")
            except:
                messages.error(request,"Failed to edit post")
            return HttpResponseRedirect(reverse("edit_post_for_students",kwargs={"post_id":post_id}))


def add_tag(request):
    return render(request,"student_template/add_tag.html")

def add_tag_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        tag=request.POST.get("tag")
        try:
            tag_model=Post_category(name=tag)
            tag_model.save()
            messages.success(request,"Successfully tag Added")
            return HttpResponseRedirect(reverse("add_tag_for_students"))
        except Exception as e:
            messages.error(request,"Failed To Add tag")
            return HttpResponseRedirect(reverse("add_tag_for_students"))






# class AddPost(CreateView):
#     model = Post
#     form_class = PostForm
#     template_name = 'student_template/add_post.html'
#     success_url = reverse_lazy('admin_home')

# class UpdatePost(UpdateView):
#     model=Post
#     form_class = EditForm
#     template_name = 'student_template/edit_post.html'
#     success_url = reverse_lazy('admin_home')

class DeletePost(DeleteView):
    model = Post
    template_name = 'student_template/delete_post.html'
    success_url = reverse_lazy('student_home')

def manage_post(request):
    posts=Post.objects.filter(author=request.user.id)
    return render(request,"student_template/manage_post.html",{"posts":posts})
