from django.conf.urls import url
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

app_name = "users"
urlpatterns = [
    path('login', views.login, name='login'),    
    path('register', views.register, name='register'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
