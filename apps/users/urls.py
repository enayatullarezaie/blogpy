from django.urls import path
from .views import *


app_name= "users"
urlpatterns =[
   path("register/", user_register, name='user-register'),
   path("login/", UserLogin.as_view(), name='user-login'),
   path("logout/", user_logout, name='user-logout'),
   path("edit/", UserEdit.as_view(), name='user-edit'),
]

