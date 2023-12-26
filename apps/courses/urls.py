from django.urls import path
from . import views



urlpatterns=[
   path('', views.root),
   path('<int:pk>', views.get_cource_detail),
   path('new-course', views.new_cource, name='new-course'),
]