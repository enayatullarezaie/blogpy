# from django.conf.urls import url
from django.urls import path, re_path

from . import views

urlpatterns =[
   re_path(r'^$', views.IndexPage.as_view(), name= 'index')
]