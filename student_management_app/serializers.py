# from django.contrib.auth.models import User, Group
# from rest_framework import serializers
# from .models import *

# class CustomSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['url', 'username', 'email', 'groups']

# class StaffsSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Staffs
#         fields = ['address','admin']


# class CoursesSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Courses
#         fields = ['course_name','created_at','updated_at']


# class SubjectsSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Subjects
#         fields = ['subject_name','course_id','staff_id']

    
# class SessionYearModelSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = SessionYearModel
#         fields =  ['session_start_year','session_end_year']

# class StudentsSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Students
#         fields =  "__all__"


