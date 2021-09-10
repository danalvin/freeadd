from django.conf.urls import url
from django.urls import path, re_path

from . import views

app_name = "users"
urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),    
    re_path(r"^~update/$", view=views.UserUpdateView.as_view(), name="update"),
    path('logout', views.LogoutView.as_view(), name='logout'),

]
