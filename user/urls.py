from django.urls import path
from .views import *


urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('email-verify',VerifyEmail.as_view(),name='email-verify'),
    path('reset-pass/',ResetPassword.as_view(),name='reset-pass'),
    path('change-pass',cheange_password,name='change-pass'),
    path('password_change/',PasswordChange.as_view(),name='password_change'),
    path('login/',LoginAPIView.as_view(),name='login'),
    path('logout/',LogoutAPIView.as_view(),name='logout'),
]

    