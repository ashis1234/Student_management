from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import *
from django.urls import reverse_lazy,reverse
from .forms import PostForm,EditForm
from django.http import HttpResponseRedirect
from student_management_app.models import CustomUser
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q 




def SearchView(query=None):
	queryset = []
	queries = query.split(" ") 
	for q in queries:
		posts = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q) | Q(category__icontains=q))
		for post in posts:
			queryset.append(post)
	return list(set(queryset))	


BLOG_POSTS_PER_PAGE = 3
def Homeview(request, *args, **kwargs):
	
	context = {}
	context['search'] = True
	# Search
	query = ""
	if request.GET:
		query = request.GET.get('q', '')
		context['query'] = str(query)
	blog_posts = sorted(SearchView(query), key=attrgetter('post_date'), reverse=True)
	cat_menu = Post_category.objects.all()
	context['cat_menu'] = cat_menu
	# Pagination
	page = request.GET.get('page', 1)
	blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)
	try:
		blog_posts = blog_posts_paginator.page(page)
	except PageNotAnInteger:
		blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
	except EmptyPage:
		blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)
	context['blog_posts'] = blog_posts
	return render(request, "home1.html", context)


def category_view(request,cats):
	context = {}
	cat_menu = Post_category.objects.all()
	context['cat_menu'] = cat_menu
	blog_posts = Post.objects.filter(category = cats)
	page = request.GET.get('page', 1)
	blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)
	try:
		blog_posts = blog_posts_paginator.page(page)
	except PageNotAnInteger:
		blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
	except EmptyPage:
		blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

	context['blog_posts'] = blog_posts
	return render(request, "home1.html", context)




def LikeView(request,pk):
	if request.POST.get('post_id') != "-1":
		post = get_object_or_404(Post,id=request.POST.get('post_id'))
		if post.dislikes.filter(id = request.user.id).exists():
			post.dislikes.remove(request.user)	
		post.likes.add(request.user)
	return HttpResponseRedirect(reverse('article',args=[str(pk)]))

def DisLikeView(request,pk):
	if request.POST.get('post_id') != "-1":
		post = get_object_or_404(Post,id=request.POST.get('post_id1'))
		if post.likes.filter(id = request.user.id).exists():
			post.likes.remove(request.user)
		post.dislikes.add(request.user)
	return HttpResponseRedirect(reverse('article',args=[str(pk)]))




	
def Articledetails(request,pk):
	cat_menu = Post_category.objects.all()
	context = {}
	context['cat_menu'] = cat_menu
	post = Post.objects.filter(id = pk)[0]
		
	context['comments'] = Comment.objects.filter(post_id = post.id)

	if request.method=='POST':
		try:
			parent_id = int(request.POST.get('parent_id'))
		except:
			parent_id = None

		content_data = request.POST.get("content")
		if len(content_data) > 0:
			parent_obj = None
			if parent_id:
				parent_qs = Comment.objects.filter(id=parent_id)
				if parent_qs.exists() and parent_qs.count()==1:
					parent_obj = parent_qs.first()
			Comment.objects.create(
				post_id = post.id,
				parent = parent_obj,
				user_id = request.user.id,
				content = content_data,
			)
			
	context['total_likes'] = post.total_likes()
	context['post'] = post
	return render(request,'detail.html',context)



class AddPost(CreateView):
	model = Post
	form_class = PostForm
	template_name = 'addpost.html'
	print(CustomUser.user_type)
	success_url = reverse_lazy('admin_home')

class UpdatePost(UpdateView):
	model=Post
	form_class = EditForm
	template_name = 'update_post.html'
	success_url = reverse_lazy('admin_home')

class DeletePost(DeleteView):
	model = Post
	template_name = 'delete_post.html'
	success_url = reverse_lazy('home')

