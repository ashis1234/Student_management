from django.conf.urls.static import static
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from blog.views import *
from student_management_app import views, HodViews, StaffViews, StudentViews
from django.conf import settings
from .views import * 
from .PrincipalView import *
from .HodViews import *

urlpatterns = [
    path('signup_principal',views.signup_principal,name="signup_principal"),
    path('signup_admin',views.signup_admin,name="signup_hod"),
    path('signup_student',views.signup_student,name="signup_student"),
    path('signup_staff',views.signup_staff,name="signup_staff"),
    path('do_principal_signup',views.do_principal_signup,name="do_principal_signup"),
    path('do_hod_signup',views.do_hod_signup,name="do_hod_signup"),
    path('do_staff_signup',views.do_staff_signup,name="do_staff_signup"),
    path('do_signup_student',views.do_signup_student,name="do_signup_student"),
    path('',views.ShowLoginPage,name="show_login"),
    path('logout_user', views.logout_user,name="logout_user"),
    path('doLogin',views.doLogin,name="do_login"),
    path('admin_home',HodViews.Hod_home,name="admin_home"),
    path('principal_home',principal_home,name="principal_home"),
    

    path('add_department/', add_department,name="add_department"),
    path('add_department_save', add_department_save,name="add_department_save"),
    path('edit_department/<str:dept_id>', edit_department,name="edit_department"),
    path('edit_department_save', edit_department_save,name="edit_department_save"),
    path('manage_department', manage_department,name="manage_department"),
    path('manage_staff', manage_staff,name="manage_staff"),
    path('edit_staff/<str:staff_id>', edit_staff,name="edit_staff"),
    path('edit_staff_save', edit_staff_save,name="edit_staff_save"),
    path('add_session_save', add_session_save,name="add_session_save"),
    path('manage_session', manage_session,name="manage_session"),
    path('check_email_exist', check_email_exist,name="check_email_exist"),
    path('check_username_exist', check_username_exist,name="check_username_exist"),
    path('staff_feedback_message', staff_feedback_message,name="staff_feedback_message"),
    path('staff_feedback_message_replied', staff_feedback_message_replied,name="staff_feedback_message_replied"),
    path('student_leave_view', student_leave_view,name="student_leave_view"),
    path('staff_leave_view', staff_leave_view,name="staff_leave_view"),
    path('staff_disapprove_leave/<str:leave_id>', staff_disapprove_leave,name="staff_disapprove_leave"),
    path('staff_approve_leave/<str:leave_id>', staff_approve_leave,name="staff_approve_leave"),
    path('edit_hod/<int:hod_id>', edit_hod,name="edit_hod"),
    path('edit_hod_save', edit_hod_save,name="edit_hod_save"),
    

    path('add_subject', HodViews.add_subject,name="add_subject"),
    path('add_subject_save', HodViews.add_subject_save,name="add_subject_save"),
    path('manage_student', HodViews.manage_student,name="manage_student"),
    path('manage_subject', HodViews.manage_subject,name="manage_subject"),
    path('edit_student/<str:student_id>', HodViews.edit_student,name="edit_student"),
    path('edit_student_save', HodViews.edit_student_save,name="edit_student_save"),
    path('edit_subject/<str:subject_id>', HodViews.edit_subject,name="edit_subject"),
    path('edit_subject_save', HodViews.edit_subject_save,name="edit_subject_save"),
    path('student_approve_leave/<str:leave_id>', student_approve_leave,name="student_approve_leave"),
    path('student_disapprove_leave/<str:leave_id>', student_disapprove_leave,name="student_disapprove_leave"),
    path('student_feedback_message', student_feedback_message,name="student_feedback_message"),
    path('student_feedback_message_replied', student_feedback_message_replied,name="student_feedback_message_replied"),
    path('admin_view_attendance', HodViews.admin_view_attendance,name="admin_view_attendance"),
    path('admin_get_attendance_dates', HodViews.admin_get_attendance_dates,name="admin_get_attendance_dates"),
    path('admin_get_attendance_student', HodViews.admin_get_attendance_student,name="admin_get_attendance_student"),
    
    path('delete/<str:type>/<int:id>',Delete,name='delete'),
    path('staff_home', StaffViews.staff_home, name="staff_home"),
    path('staff_take_attendance', StaffViews.staff_take_attendance, name="staff_take_attendance"),
    path('staff_update_attendance', StaffViews.staff_update_attendance, name="staff_update_attendance"),
    path('get_students', StaffViews.get_students, name="get_students"),
    path('get_attendance_dates', StaffViews.get_attendance_dates, name="get_attendance_dates"),
    path('get_attendance_student', StaffViews.get_attendance_student, name="get_attendance_student"),
    path('save_attendance_data', StaffViews.save_attendance_data, name="save_attendance_data"),
    path('save_updateattendance_data', StaffViews.save_updateattendance_data, name="save_updateattendance_data"),
    path('assignment_check', StaffViews.assignment_check, name="assignment_check"),
    path('get_students_assignment', StaffViews.get_students_assignment, name="get_students_assignment"),
    
    path('assignment_upload',StaffViews.Assignment_upload,name="assignment_upload"),
    path('apply_leave', apply_leave, name="apply_leave"),
    path('apply_leave_save', apply_leave_save, name="apply_leave_save"),
    path('feedback', feedback, name="feedback"),
    path('feedback_save', feedback_save, name="feedback_save"),
    path('staff_profile', StaffViews.staff_profile, name="staff_profile"),
    path('staff_profile_save', StaffViews.staff_profile_save, name="staff_profile_save"),


    path('student_home', StudentViews.student_home, name="student_home"),
    path('student_view_attendance', StudentViews.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post', StudentViews.student_view_attendance_post, name="student_view_attendance_post"),
    path('student_profile', StudentViews.student_profile, name="student_profile"),
    path('student_profile_save', StudentViews.student_profile_save, name="student_profile_save"),
    path('assignment_view',StudentViews.assignment_view,name="assignment_view"),
    path('assignment_submit/<int:id>',StudentViews.assignment_submit,name="assignment_submit"),
    path('assignment_save',StudentViews.assignment_save,name="assignment_save"),
    
]