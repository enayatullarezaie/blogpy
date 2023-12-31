from django.urls import path, re_path
from . import views


app_name= "blog"
urlpatterns =[
   path('', views.IndexPage.as_view(), name= 'home-blog'),
   path('search/', views.search, name= 'search'),
   path('contact/', views.ContactPage.as_view(), name= 'contact'),
   path('about/', views.AboutPage.as_view(), name= 'about'),
   path('category/', views.CategoryPage.as_view(), name= 'category'),
   re_path(r'article/(?P<slug>[-\w]+)/', views.ArticleDetail.as_view(), name= 'detail'),
   path('like/', views.LikeHandler.as_view(), name= 'like'),

   path('api/article/all/', views.AllArticlesAPIView.as_view(), name= 'all_articles'),
   path('api/article/', views.SingleArticleAPIView.as_view(), name= 'single_article'),
   path('api/article/search/', views.SearchArticleAPIView.as_view(), name= 'search_article'),
   path('api/article/submit/', views.SubmitArticleAPIView.as_view(), name= 'submit_article'),
   path('api/article/update-cover/', views.UpdateArticleAPIView.as_view(), name= 'update_article'),
   path('api/article/delete/', views.DeleteArticleAPIView.as_view(), name= 'delete_article'),

   path('sidebar/', views.sidebar, name= 'sidebar'),
]




