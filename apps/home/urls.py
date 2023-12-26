from django.urls import path
from . import views


urlpatterns=[
   path('', views.gethome, name='home-page')
]