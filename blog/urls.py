from django.urls import path
from .views import *


urlpatterns = [
    path('', Homeview,name='home'),
    path('article/<int:pk>/',Articledetails,name='article'),
    path('like/<int:pk>/',LikeView,name='like_post'),
    path('dislike/<int:pk>/',DisLikeView,name='dislike_post'),
    path('article/<int:pk>/remove/',DeletePost.as_view(),name='delete_post'),
    path('category/<str:cats>/',category_view,name='category'),
    path('search/', SearchView,name='search'),
]


