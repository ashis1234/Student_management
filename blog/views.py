from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import *
from django.contrib import messages
from django.urls import reverse_lazy,reverse
from .forms import PostForm,EditForm
from django.http import HttpResponseRedirect,HttpResponse,Http404
from student_management_app.models import *
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q 
from .forms import PasswordChange
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from students_management_project.settings import ITEM_PER_PAGE
from django.contrib.postgres.search import SearchVector
from django.views.decorators.csrf import csrf_exempt



def SearchView(blog_posts,query=None):
	queryset = []
	queries = query.split(" ") 
	for q in queries:
		posts = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
		for post in posts:
			queryset.append(post)	
	res = []
	for post in queryset:
		if post in blog_posts:
			res.append(post)
	return 	res


def get_most_likes_post(order=1):
	blog_posts = []
	for post in Post.objects.all():
		blog_posts.append([post.total_likes,str(post.title),post])
	
	if order:
		blog_posts.sort(reverse=True)
	else:
		blog_posts.sort()
	most_like_post = [post[2] for post in blog_posts]
	return most_like_post


BLOG_POSTS_PER_PAGE = 8

def get_top_post():
	context = {}
	cat_menu = Category.objects.all()
	context['cat_menu'] = cat_menu
	# featured
	featured_posts = Post.objects.filter(featured=True)
	min_size = min(5,len(featured_posts))
	featured_posts = featured_posts[:min_size]
	context['featured_posts'] = featured_posts

	#most view 
	most_view_posts = Post.objects.order_by('-view_count')
	min_size = min(5,len(most_view_posts))
	most_view_posts = most_view_posts[:min_size]
	context['most_view_posts'] = most_view_posts

	# latest_post
	latest_posts = Post.objects.order_by('post_date')
	min_size = min(5,len(latest_posts))
	latest_posts = latest_posts[:min_size]
	context['latest_posts'] = latest_posts

	# most like post
	context['most_like_posts'] = get_most_likes_post()

	trending_topic = Category.objects.order_by('-count')
	min_size = min(15,len(trending_topic))
	trending_topic = trending_topic[:min_size]
	
	context['trending_topic1'] = trending_topic
		

	return context

def HomeviewUtill(request,blog_posts):
	
	context = get_top_post()
	context['search'] = True
	# user = User.objects.get(id=5)
	
	# for ass in Assignment.objects.all():
	# 	ass.staff = user
	# 	ass.save()
	# for ass in Assignment.objects.all():
	# 	print(ass.staff)

	# print(request.user.id)

	for user in User.objects.all():
		print(user.username,user.user_type)
	print()
	# for user in Principal.objects.all():
	# 	print(user.admin.username)
	# print()
	# for user in HOD.objects.all():
	# 	print(user.admin.username)
	# print()
	# for user in Staffs.objects.all():
	# 	print(user.admin.username)
	# print()
	# for user in Students.objects.all():
	# 	print(user.admin.username)
	# Search
	query = ""
	if request.GET:
		query = request.GET.get('q', '')
		context['query'] = str(query)

	blog_posts = sorted(SearchView(blog_posts,query), key=attrgetter('post_date'), reverse=True)
	# Pagination
	context['pagination_req'] = len(blog_posts) > BLOG_POSTS_PER_PAGE
	page = request.GET.get('page', 1)
	blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)
	try:
		blog_posts = blog_posts_paginator.page(page)
	except PageNotAnInteger:
		blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
	except EmptyPage:
		blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)
	context['blog_posts'] = blog_posts
	return context

def Most_view(request):

	context = HomeviewUtill(request,Post.objects.order_by('-view_count'))
	request.session['login-from'] = "most_viewed_articles"
	return render(request, "home1.html", context)

def Latest_Post(request):
	context = HomeviewUtill(request,Post.objects.order_by('-post_date'))
	request.session['login-from'] = "latest_articles"
	return render(request, "home1.html", context)
	
# def TrendingTopicView(request):
# 	context = HomeviewUtill(request,Post.objects.order_by('-post_date'))
# 	request.session['login-from'] = "trending_topic"
# 	return render(request, "home1.html", context)

def Most_Like_Post(request):
	context = HomeviewUtill(request,get_most_likes_post())
	request.session['login-from'] = "most_like_articles"
	return render(request, "home1.html", context)


def Homeview(request, *args, **kwargs):
	context = HomeviewUtill(request,Post.objects.all())
	request.session['login-from'] = 'home'
	return render(request, "home1.html", context)


def category_view(request,cats):
	cat_id = Category.objects.get(name=cats)
	p_category = Post_category.objects.filter(cat_id=cat_id)
	blog_posts = []
	try:
		for p_cat in p_category:
			blog_posts.append(Post.objects.get(id=p_cat.post_id.id))
	except Exception as e:
		print(e)
	context = HomeviewUtill(request,blog_posts)
	request.session['login-from'] = 'category'
	request.session['item-id'] = cats
	request.session['subpath'] = 'cats'
	return render(request, "home1.html", context)


def Featured_view(request):
	post = Post.objects.filter(featured=True)
	context = HomeviewUtill(request,post)
	request.session['login-from'] = "featured_articles"
	return render(request, "home1.html", context)




def LikeView(request,pk):
	if request.POST.get('post_id') != "-1":
		post = get_object_or_404(Post,id=request.POST.get('post_id'))
		if post.dislikes.filter(id = request.user.id).exists():
			post.dislikes.remove(request.user)	
		post.likes.add(request.user)
	return HttpResponseRedirect(reverse('article',args=[str(pk)]))





	
def Articledetails(request,pk,cmnt_id=None):
	request.session['login-from'] = 'article'
	request.session['item-id'] = pk
	request.session['subpath'] = 'pk'
	context = get_top_post()
	post = Post.objects.filter(id = pk)[0]
	context['comments'] = Comment.objects.filter(post_id = post.id)
	context['post'] = post
	return render(request,'detail.html',context)




# class AddPost(CreateView):
# 	model = Post
# 	form_class = PostForm
# 	template_name = 'addpost.html'
# 	print(User.user_type)
# 	success_url = reverse_lazy('admin_home')

# class UpdatePost(UpdateView):
# 	model=Post
# 	form_class = EditForm
# 	template_name = 'update_post.html'
# 	success_url = reverse_lazy('admin_home')

# class DeletePost(DeleteView):
# 	model = Post
# 	template_name = 'delete_post.html'
# 	success_url = reverse_lazy('home')


def add_post(request):
	user_type = request.session.get('user_type',-1)
	if user_type == -1:
		raise Http404('method not allowed')
	form = PostForm()
	if request.method != 'POST':
		return render(request,'add_post.html',{'form' : form})
	else:
		form = PostForm(request.POST)
		if form.is_valid():
			user_id = request.user.id
			title = form.cleaned_data['title']
			body = form.cleaned_data['body']
			category = form.cleaned_data['category']
			featured = form.cleaned_data['featured']
			user = User.objects.get(id=user_id)
			category1 = []
			if Post.objects.filter(title=title).exists():
				messages.error(request,"Title already exists")
				return HttpResponseRedirect(reverse("add_post"))
			
			
			for cat in category:
				if Category.objects.filter(name=cat).exists():
					cat1 = Category.objects.get(name=cat)
					cat1.count+=1
					cat1.save()
					category1.append(cat1)
					pass
				else:
					cat1 = Category.objects.create(name=cat,count=1)
					category1.append(cat1)

			try:
				post = Post.objects.create(body=body,title=title,author=user,category=category1,featured=featured,view_count=0)
				post.save()
				try:
					for cat in category1:
						p_cat = Post_category.objects.get_or_create(cat_id = cat,post_id=post)
				except Exception as e:
					print(e)
				messages.success(request,"Successfully Added Post")
			except:
				messages.error(request,"Failed to added Post")
			return HttpResponseRedirect(reverse("add_post"))
		else:
			return HttpResponseRedirect(reverse("add_post"))

def manage_category(request):
	user_type = request.session.get('user_type',-1)
	if user_type == -1 or user_type == '0':
		raise Http404('method not allowed')
	categorys=Category.objects.filter()
	context = {}
	context['pagination_req'] = len(categorys) > ITEM_PER_PAGE
	page = request.GET.get('page', 1)
	categorys_paginator = Paginator(categorys, ITEM_PER_PAGE)
	try:
	    categorys = categorys_paginator.page(page)
	except PageNotAnInteger:
	    categorys = categorys_paginator.page(ITEM_PER_PAGE)
	except EmptyPage:
		  	categorys = categorys_paginator.page(categorys_paginator.num_pages)
	context['categorys'] = categorys
	return render(request,"manage_category.html",context)


def edit_post(request,post_id):
	user_type = request.session.get('user_type',-1)
	if user_type == -1:
		raise Http404('method not allowed')
	request.session['post_id']=post_id
	post=Post.objects.get(id=post_id)
	form=EditForm()
	form.fields['title'].initial=post.title
	form.fields['body'].initial=post.body
	form.fields['category'].initial=post.category
	form.fields['featured'].initial = post.featured
	return render(request,"edit_post.html",{"form":form,"id":post_id})

def edit_post_save(request):
	user_type = request.session.get('user_type',-1)
	if user_type == -1:
		raise Http404('method not allowed')
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
			body = form.cleaned_data['body']
			category = form.cleaned_data['category']
			featured = form.cleaned_data['featured']
			user = User.objects.get(id=user_id)
			post = Post.objects.get(id=post_id)
			
			if post.title != title and Post.objects.filter(title=title).exists():
				messages.error(request,"Title already exists")
				return HttpResponseRedirect(reverse("edit_post",kwargs={"post_id":post_id}))
			
	
			category1 = []
			category2 = []
			
			for cat in category:
				category2.append(cat)
				if Category.objects.filter(name=cat).exists():
					cat_obj = Category.objects.get(name=cat)
					cat_obj.count+=1
					cat_obj.save()
					category1.append(cat_obj)
				else:
					cat_obj = Category.objects.create(name=cat,count=1)
					category1.append(cat_obj)
			
			try:
				for p_cat in post.category:
					if p_cat not in category2:
						cat_obj = Category.objects.get(name=p_cat)
						p_cat_obj = Post_category.objects.get(post_id=post,cat_id = cat_obj)
						p_cat_obj.delete()
						cat_obj.count-=1
						if cat_obj.count == 0:
							cat_obj.delete()
			except Exception as e:
				print(e)
			try:
				print(category1)
				post.title = title
				post.body = body
				post.category = category1
				post.featured = featured
				post.save()
				for cat in category1:
					p_cat = Post_category.objects.get_or_create(cat_id = cat,post_id=post)
				if 'post_id' in request.session:
					del request.session['post_id']
				messages.success(request,"Successfully post edited")
			except Exception as e:
				print()
				print(e)
				print()
				messages.error(request,"Failed to edit post")
				return HttpResponseRedirect(reverse("edit_post",kwargs={"post_id":post_id}))	
		return HttpResponseRedirect(reverse("edit_post",kwargs={"post_id":post_id}))	






class DeletePost(DeleteView):
	model = Post
	template_name = 'delete_post.html'
	success_url = reverse_lazy('manage_post')

def manage_post(request):
	user_type = request.session.get('user_type',-1)
	if user_type == -1:
		raise Http404('method not allowed')
	posts=Post.objects.filter(author=request.user.id)
	context = {}
	context['pagination_req'] = len(posts) > ITEM_PER_PAGE
	page = request.GET.get('page', 1)
	posts_paginator = Paginator(posts, ITEM_PER_PAGE)
	try:
	    posts = posts_paginator.page(page)
	except PageNotAnInteger:
	    posts = posts_paginator.page(ITEM_PER_PAGE)
	except EmptyPage:
		  	posts = posts_paginator.page(posts_paginator.num_pages)
	context['posts'] = posts
	return render(request,"manage_post.html",context)

@csrf_exempt
def AddComments(request):
	post_id = int(request.POST.get('post_id'))
	user_id = int(request.POST.get('user_id'))
	parent_comment_id = int(request.POST.get("parent_id"))
	node_id = int(request.POST.get("node_id"))
	message = request.POST.get("message")
	if node_id:
		cmnt = Comment.objects.get(id=parent_comment_id)
		cmnt.content = message
		cmnt.add_comment = timezone.now()
		cmnt.save()
		return HttpResponse("Post Edited Succesfully")


	post = Post.objects.get(id=post_id)
	user = User.objects.get(id=user_id)
	parent = None
	if parent_comment_id:
		parent = Comment.objects.get(id=parent_comment_id)
	try:
		Comment.objects.create(post=post,parent=parent,content=message,user=user)
		return HttpResponse("True")
	except Exception as e:
		print(e)
		return HttpResponse("False")

@csrf_exempt
def DisLikeView(request):
	post_id = int(request.POST.get('post_id'))
	user_id = int(request.POST.get('user_id'))
	post = get_object_or_404(Post,id=post_id)
	user_obj = User.objects.get(id=user_id)
	if post.author.id == user_id:
		return HttpResponse("same user")
	try:
		if post.likes.filter(id = user_id).exists():
			post.likes.remove(user_obj)
		if post.dislikes.filter(id=user_id).exists():
			return HttpResponse('already')
		post.dislikes.add(user_obj)
	except Exception as e:
		print(e)
		return HttpResponse("False")
	return HttpResponse("True")


@csrf_exempt
def LikeView(request):
	post_id = int(request.POST.get('post_id'))
	user_id = int(request.POST.get('user_id'))
	post = get_object_or_404(Post,id=post_id)
	user_obj = User.objects.get(id=user_id)
	try:
		print(post.author.id,user_id)
		if post.author.id == user_id:
			print("FF")
			return HttpResponse("same user")
		if post.dislikes.filter(id = user_id).exists():
			post.dislikes.remove(user_obj)
		if post.likes.filter(id=user_id).exists():
			return HttpResponse('already')
		post.likes.add(user_obj)
	except Exception as e:
		print(e)
		return HttpResponse("False")
	return HttpResponse("True")


@csrf_exempt
def LikeCommentView(request):
	post_id  = int(request.POST.get('post_id'))
	user_id  = int(request.POST.get('user_id'))
	cmnt_id=int(request.POST.get('cmnt_id'))
	user_obj = User.objects.get(id=user_id)
	cmnt_obj = Comment.objects.get(id=cmnt_id)
	if cmnt_obj.user.id == user_id:
		return HttpResponse("same user")
	try:
		if cmnt_obj.dislikes.filter(id = user_id).exists():
			cmnt_obj.dislikes.remove(user_obj)
		if cmnt_obj.likes.filter(id=user_id).exists():
			return HttpResponse('already')
		cmnt_obj.likes.add(user_obj)
	except Exception as e:
		print(e)
		return HttpResponse("False")
	return HttpResponse("True")


@csrf_exempt
def DisLikeCommentView(request):
	post_id  = int(request.POST.get('post_id'))
	user_id  = int(request.POST.get('user_id'))
	cmnt_id=int(request.POST.get('cmnt_id'))
	user_obj = User.objects.get(id=user_id)
	cmnt_obj = Comment.objects.get(id=cmnt_id)
	if cmnt_obj.user.id == user_id:
		return HttpResponse("same user")
	try:
		if cmnt_obj.likes.filter(id = user_id).exists():
			cmnt_obj.likes.remove(user_obj)
		if cmnt_obj.dislikes.filter(id=user_id).exists():
			return HttpResponse('already')
		cmnt_obj.dislikes.add(user_obj)
	except Exception as e:
		print(e)
		return HttpResponse("False")
	return HttpResponse("True")


