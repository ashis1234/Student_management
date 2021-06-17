from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime,date
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.contenttypes.models import ContentType
from mptt.models import MPTTModel, TreeForeignKey
from student_management_app.models import CustomUser


		

class Post_category(models.Model):
	name = models.CharField(max_length=255)
	def __str__(self):
		return self.name
	
class Post(models.Model):
	title        = models.CharField(max_length=250)
	title_tag    = models.CharField(max_length=250,default="Ashis Blog")
	author       = models.ForeignKey(CustomUser,on_delete = models.CASCADE)
	body         = RichTextField(blank=True,null=True)
	post_date    = models.DateField(auto_now_add = True)
	category     = models.CharField(max_length=255,default = 'coding')
	likes        = models.ManyToManyField(CustomUser,related_name = 'post_like')
	dislikes     = models.ManyToManyField(CustomUser,related_name = 'post_dislike')
	
	@property
	def get_content_type(self):
		return ContentType.objects.get_for_model(self.__class__)
	
	def total_likes(self):
		return self.likes.count() - self.dislikes.count()
		
	def __str__(self):
		return self.title + '|' + str(self.author)

	def get_absolute_url(self):
		return reverse('article',args = (str(self.id)))


class Comment(MPTTModel):
	post        =  models.ForeignKey(Post,null=True,on_delete=models.CASCADE)
	user        =  models.ForeignKey(CustomUser,null=True,on_delete=models.CASCADE)
	parent      =  TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
	add_comment =  models.DateTimeField(auto_now_add=True)
	content     =  models.TextField(default="sssssss")

	class MPTTMeta:
		order_insertion_by = ['add_comment']
