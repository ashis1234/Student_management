from django.urls import path,re_path

from .views import *
from student_management_app.views import *

urlpatterns = [
    path('', Homeview,name='home'),
    path('article/<int:pk>/',Articledetails,name='article'),
    

   


    path('like_post/',LikeView,name='like_post'),
    path('dislike_post/',DisLikeView,name='dislike_post'),
    path('like_comment/',LikeCommentView,name='like_comment'),
    path('dislike_comment/',DisLikeCommentView,name='dislike_comment'),
    path('article/<int:pk>/remove/',DeletePost.as_view(),name='delete_post'),
    path('category/<str:cats>/',category_view,name='category'),
    path('search/', SearchView,name='search'),
    path('manage_category/',manage_category,name="manage_category"),
    path('add_post',add_post,name = "add_post"), 
    path('edit_post/<str:post_id>',edit_post,name = "edit_post"),
    path('edit_post_save', edit_post_save,name="edit_post_save"),
    path('delete_post/<int:pk>',DeletePost.as_view(),name = "delete_post"),
    path('manage_post',manage_post,name = "manage_post"),
    path('featured_articles/',Featured_view,name="featured_articles"),
    path('most_viewed_articles/',Most_view,name="most_viewed_articles"),
    path('latest_articles/',Latest_Post,name="latest_articles"),
    # path('trending_topic/',TrendingTopicView,name="trending_topic"),
    path('most_like_articles/',Most_Like_Post,name="most_like_articles"),
    path('add_new_comments/',AddComments,name="add_new_comments"),
    path('profile/<str:user>/',ProfileView,name="user_profile"),
]


