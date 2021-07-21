from django.contrib.auth.forms import SetPasswordForm
from django import forms
from django.core import validators
from .models import *
from student_management_app.models import CustomUser
from django_mysql.forms import SimpleListField


class PasswordChange(SetPasswordForm):
	class Meta:
		model = CustomUser
		fields = ('new_password1','new_password2')
			
	def __init__(self, *arg,**kwargs):
		super(PasswordChange, self).__init__(*arg,*kwargs)
		self.fields['new_password1'].widget.attrs['class'] = 'form-control'
		self.fields['new_password2'].widget.attrs['class'] = 'form-control'


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title','category','body','featured')

		widgets  = {
			'title': forms.TextInput(attrs={'class' : 'form-control','placeholder' : 'Enter title of the blog'}),
			'category' : forms.TextInput(attrs={'class' : 'form-control','placeholder' : 'Enter tag sepearted by comma'}),
			'body' : forms.Textarea(attrs={'class' : 'form-control','cols': 80, 'rows': 20})
		}

#
class EditForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title','category','body')

		fields = ('title','category','body','featured')

		widgets  = {
			'title': forms.TextInput(attrs={'class' : 'form-control','placeholder' : 'Enter title of the blog'}),
			'category' : forms.TextInput(attrs={'class' : 'form-control','placeholder' : 'Enter tag sepearted by comma'}),
			'body' : forms.Textarea(attrs={'class' : 'form-control','cols': 80, 'rows': 20})
		}