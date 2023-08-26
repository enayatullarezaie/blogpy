# from django.conf.urls import url
from django.urls import path, re_path

from . import views

urlpatterns =[
   path('', views.IndexPage.as_view(), name= 'index'),
   path('contact/', views.ContactPage.as_view(), name= 'contact'),
]