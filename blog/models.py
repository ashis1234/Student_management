from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime,date
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.contenttypes.models import ContentType
from mptt.models import MPTTModel, TreeForeignKey
from student_management_app.models import CustomUser
from django_mysql.models import ListCharField
import math

		


	
class Post(models.Model):
	title        = models.CharField(max_length=250)
	author       = models.ForeignKey(CustomUser,on_delete = models.CASCADE)
	body         = RichTextField(blank=True,null=True)
	post_date    = models.DateTimeField(auto_now_add = True)
	likes        = models.ManyToManyField(CustomUser,related_name = 'post_like')
	category     = ListCharField(base_field=models.CharField(max_length=10),size=6,max_length=(6 * 11),null=True)
	view_count   = models.IntegerField(default=0)
	dislikes     = models.ManyToManyField(CustomUser,related_name = 'post_dislike')
	featured     = models.BooleanField(default=False)
	updated_at   = models.DateTimeField(auto_now_add=True)


	@property
	def view_added(self):
		print("added")
		count = self.view_count + 1
		post = Post.objects.get(id=self.id)
		post.view_count = count
		post.save()

	@property
	def total_likes(self):
		return self.likes.count() - self.dislikes.count()
	@property
	def total_likes_pos(self):
		c = self.likes.count() - self.dislikes.count()
		print(c)
		return c >= 0
	def get_likes(self):
		return self.likes.count()
	def get_dislikes(self):
		return self.dislikes.count()
		
	def __str__(self):
		return self.title + '|' + str(self.author)

	def get_absolute_url(self):
		return reverse('article',args = (str(self.id)))
	
	@property
	def whenpublished(self):
    
		now = timezone.now()
		if self.post_date is not None:
			diff = now - self.post_date

			if diff.days == 0 and 0 <= diff.seconds < 60:
				seconds = diff.seconds
				if seconds == 1:
					return str(seconds) + "second ago"
				else:
					return str(seconds) + " seconds ago"

			if diff.days == 0 and 60 <= diff.seconds < 3600:
				minutes = math.floor(diff.seconds / 60)

				if minutes == 1:
					return str(minutes) + " minute ago"
				else:
					return str(minutes) + " minutes ago"

			if diff.days == 0 and 3600 <= diff.seconds < 86400:
				hours = math.floor(diff.seconds / 3600)

				if hours == 1:
					return str(hours) + " hour ago"

				else:
					return str(hours) + " hours ago"

            # 1 day to 30 days
			if 1 <= diff.days < 30:
				days = diff.days

				if days == 1:
					return str(days) + " day ago"

				else:
					return str(days) + " days ago"

			if 30 <= diff.days < 365:
				months = math.floor(diff.days / 30)

				if months == 1:
					return str(months) + " month ago"

				else:
					return str(months) + " months ago"

			if diff.days >= 365:
				years = math.floor(diff.days / 365)

				if years == 1:
					return str(years) + " year ago"

				else:
					return str(years) + " years ago"


class Category(models.Model):
	name = models.CharField(max_length=50)
	count = models.IntegerField(default=0)
	def __str__(self):
		return self.name


class Post_category(models.Model):
	cat_id = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='category',default=0)
	post_id = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post')
	



class Comment(MPTTModel):
	post        =  models.ForeignKey(Post,null=True,on_delete=models.CASCADE)
	user        =  models.ForeignKey(CustomUser,null=True,on_delete=models.CASCADE)
	likes       =  models.ManyToManyField(CustomUser,related_name = 'comment_like')
	dislikes    =  models.ManyToManyField(CustomUser,related_name = 'comment_dislike')
	parent      =  TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
	add_comment =  models.DateTimeField(auto_now_add=True)
	content     =  models.TextField(default="sssssss")
	updated_at  = models.DateTimeField(auto_now_add=True)

	class MPTTMeta:
		order_insertion_by = ['-add_comment']

	@property
	def total_likes(self):
		return self.likes.count() - self.dislikes.count()
	def get_likes(self):
		return self.likes.count()
	def get_dislikes(self):
		return self.dislikes.count()
	@property
	def get_comment_url(self):
		return "#comment_"+str(self.id)