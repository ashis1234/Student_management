from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
router = routers.DefaultRouter()

# router.register(r'sessionyear', SessionYearModelViewSet)
# router.register(r'courses', CoursesViewSet)
# router.register(r'subjects', SubjectsViewSet)
# router.register(r'staffs', StaffsViewSet)
# router.register(r'customuser', CustomUSerViewSet)
# router.register(r'students', StudentsViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include(router.urls)),
    # path('api/gettoken/',TokenObtainPairView.as_view(),name="gettoken"),
    # path('api/resfresh_token/',TokenRefreshView.as_view(),name="refresh_token"),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    path('', include('blog.urls')),
    path('backend/',include('student_management_app.urls')),
    path('members/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
