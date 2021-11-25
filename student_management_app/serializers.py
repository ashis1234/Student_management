from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *
from user.models import User

class CustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','url', 'username', 'email', 'groups']
    
    def create(self, validated_data):
        return User(**validated_data)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id','dept_name','created_at','updated_at']
    
    def create(self, validated_data):
        return Department(**validated_data)


class PrincipalSerializer(serializers.HyperlinkedModelSerializer):
    admin = CustomSerializer(many=False,read_only=True)
    class Meta:
        model = Staffs
        fields = ['id','admin','created_at']
        depth = 1
    

class StaffsSerializer(serializers.HyperlinkedModelSerializer):
    admin = CustomSerializer(many=False,read_only=True)
    dept_id = DepartmentSerializer(many=False,read_only=True)
    class Meta:
        model = Staffs
        fields = ['id','address','admin','created_at','dept_id']
        depth = 1

class HODsSerializer(serializers.HyperlinkedModelSerializer):
    admin = CustomSerializer(many=False)
    dept_id = DepartmentSerializer(many=False)
    class Meta:
        model = HOD
        fields = ['id','address','admin','created_at','dept_id']
        depth = 1



class SessionYearModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SessionYearModel
        fields =  ['id','session_start_year','session_end_year']



# Students
class StudentsSerializer(serializers.HyperlinkedModelSerializer):
    admin = CustomSerializer(many=False,read_only=True)
    dept_id = DepartmentSerializer(many=False,read_only=True)
    session_year_id = SessionYearModelSerializer(many=False,read_only=True)
    class Meta:
        model = Students
        fields = ['id','address','admin','created_at','dept_id','session_year_id']
        depth = 1


class SubjectsSerializer(serializers.HyperlinkedModelSerializer):
    dept_id = DepartmentSerializer(many=False,read_only=True)
    staff_id = StaffsSerializer(many=False,read_only=True)
    session_year = SessionYearModelSerializer(many=False,read_only=True)
    class Meta:
        model = Subjects
        fields = ['id','subject_name','dept_id','staff_id','session_year']


