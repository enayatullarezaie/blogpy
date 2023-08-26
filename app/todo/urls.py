from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.TodosViewSetAPIView)

urlpatterns =[
   path('', views.all_todos),
   path('<int:todo_id>', views.todo_detail_view),

   path('cbv/', views.TodosAPIView.as_view()),
   path('cbv/<int:todo_id>', views.TodosDetailAPIView.as_view()),

   path('mixins/', views.TodosListMixinAPIViews.as_view()),
   path('mixins/<int:pk>/', views.TodosDetailMixinAPIViews.as_view()),

   path('generics/', views.TodosGenericsAPIView.as_view()),
   path('generics/<int:pk>/', views.TodosGenericsDetailAPIView.as_view()),

   path('viewsets/', include(router.urls)),
   path('users/', views.UsersGenericAPIView.as_view( )),

]


