from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *



# Create your views here.



class IndexPage(TemplateView):

   def get(self, request, **kwargs):
      article_data = []
      all_articles = Article.objects.order_by('-created_at').all()[:9]

      for article in all_articles : 
         article_data.append({
            'title': article.title,
            'cover': article.cover.url,
            'category': article.category.title,
            'created_at': article.created_at.date(),
         })

      promote_data= []
      all_promote_articles = Article.objects.filter(promote= True)
      for article in all_promote_articles :
         if article.promote == True:
            promote_data.append({
               "title": article.title,
               "category": article.category.title,
               "author": article.author.user.first_name + ' ' + article.author.user.last_name,
               "cover": article.cover.url if article.cover else None,
               "avatar": article.author.avatar.url if article.author.avatar else None,
               "created_at": article.created_at.date(),
            })

      context = {
         'article_data': article_data,
         'promote_data': promote_data
      }
      return render(request, "index.html", context)






class ContactPage(TemplateView):
   template_name = 'page-contact.html'


