from django.urls import path
from . import views



urlpatterns =[
   path('', views.IndexPage.as_view(), name= 'index'),
   path('contact/', views.ContactPage.as_view(), name= 'contact'),
   path('about/', views.AboutPage.as_view(), name= 'about'),
   path('category/', views.CategoryPage.as_view(), name= 'category'),
   path('article/<int:pk>', views.ArticleDetail.as_view(), name= 'detail'),

   path('api/article/all/', views.AllArticlesAPIView.as_view(), name= 'all_articles'),
   path('api/article/', views.SingleArticleAPIView.as_view(), name= 'single_article'),
   path('api/article/search/', views.SearchArticleAPIView.as_view(), name= 'search_article'),
   path('api/article/submit/', views.SubmitArticleAPIView.as_view(), name= 'submit_article'),
   path('api/article/update-cover/', views.UpdateArticleAPIView.as_view(), name= 'update_article'),
   path('api/article/delete/', views.DeleteArticleAPIView.as_view(), name= 'delete_article'),
]