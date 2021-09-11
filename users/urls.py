from django.conf.urls import url
from django.urls import path, re_path

from . import views

app_name = "users"
urlpatterns = [
    path('login', views.login, name='login'),    
    path('register', views.register, name='register'),
    path('logout', views.LogoutView.as_view(), name='logout'),

]
