from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from students_management_project import settings
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/gettoken/',TokenObtainPairView.as_view(),name="gettoken"),
    # path('api/resfresh_token/',TokenRefreshView.as_view(),name="refresh_token"),
    path('api/auth/', include('rest_framework.urls')),
    path('users/',include('user.urls')),
    path('', include('blog.urls')),
    path('backend/',include('student_management_app.urls')),
    path('api/gettoken/',TokenObtainPairView.as_view(),name="gettoken"),
    path('api/refresh_token/',TokenRefreshView.as_view(),name="refresh_token"),


] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
