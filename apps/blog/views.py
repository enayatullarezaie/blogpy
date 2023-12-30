from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import TemplateView
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from django.core.paginator import Paginator


def sidebar(request): 
   context={"name": "enayat"}
   return render(request, "blog/includes/sidebar.html", context=context)


def search(request): 
   page_number= request.GET.get("page")
   if not page_number:
      page_number = 1

   query = request.GET['q']
   articles= Article.objects.filter(title__icontains= query)
   paginator = Paginator(articles, 3)
   art_list = paginator.get_page(number= page_number)

   return render(request, "blog/search.html", context={ "articles": art_list, 'q':query})


class IndexPage(TemplateView):
   def get(self, request):
      page_number= request.GET.get("page")
      if not page_number:
         page_number = 1

      articles = Article.objects.all()
      promote_arts = Article.objects.filter(promote= True)
      paginator = Paginator(articles, 3)
      art_list = paginator.get_page(number= page_number)
      context = {
         'article_list': art_list,
         'promote_data': promote_arts
      }
      return render(request, "blog/index.html", context)


class ArticleDetail(TemplateView):
   def get(self, request, slug):
      try:
         article= Article.objects.get(slug= slug)
         author = article.author
         # comments = Comment.onjects.filter(article=article)
      except:
         return HttpResponse({}, status=404)
      context={ 
         "article": article, 
         "comments":"comments", 
         "author": author,
      }
      return render( request,'blog/single-blog.html', context=context)
   
   def post(self, request, slug):
      article= Article.objects.get(slug= slug)
      text = request.POST.get("text")
      user = request.user
      if "reply" in request.POST:
         new_reply = Comment.objects.create(
            user= user,
            text = text,
            article = article,
            parent_id = request.POST["parent_id"]
         )
         return redirect( article.get_absolute_url() )

      new_comm = Comment.objects.create(
         user= user,
         text = text,
         article = article,
      )
      context={ 
         "article": article, 
      }
      return render( request,'blog/single-blog.html', context=context)


class ContactPage(TemplateView):
   template_name = 'blog/page-contact.html'


class AboutPage(TemplateView):
   template_name = 'blog/page-about.html'


class CategoryPage(TemplateView):
   template_name = 'blog/page-category.html'


class CategoryPage(TemplateView):
   template_name = 'blog/search.html'



class AllArticlesAPIView(APIView):

   def get(self, request, *args, **kwargs):
      try:
         articles = Article.objects.order_by('-created_at').all()
      except:
         return Response({'detail': 'No article found'}, status= 404)
      
      serialized = serializers.ArticleSerializer(articles, many=True)
      return Response({ "detail": serialized.data }, status.HTTP_200_OK)
      
class SingleArticleAPIView(APIView):
   def get(self, request):
      try:
         article_title = request.GET['article_title']
         article = Article.objects.filter(title__contains= article_title)
         serialized = serializers.SingleArticleSerializer(article, many= True)
         data = serialized.data

         return Response({"detail":data}, status.HTTP_200_OK)

      except:
         return Response({'detail': 'article not found'}, status= 404)

class SearchArticleAPIView(APIView):
   def get(self, request, format=None):
      try:
         # from django.db.models import QuerySet, Q
         query= request.GET['query']
         articles = Article.objects.filter(content__contains= query)
         # articles = Article.objects.filter(Q(content__icontains= query))
         data= []
         for article in articles :
            data.append({
               "title": article.title,
               "cover": article.cover.url if article.cover else None,
               "content": article.content,
               "created_at": article.created_at,
               "category": article.category.title,
               "author": article.author.user.first_name + ' ' + article.author.user.last_name,
               "promote": article.promote,
            })
         return Response({"data":data}, status.HTTP_200_OK)

      except:
         return Response({'message': 'internal server error'},status.HTTP_500_INTERNAL_SERVER_ERROR)

class SubmitArticleAPIView(APIView):
   def post(self, request, format=None):
      try:
         serializer= serializers.SubmitArticleSerializer(data= request.data)
         if serializer.is_valid() :
            title= serializer.data.get('title')
            cover= request.FILES["cover"]
            content= serializer.data.get('content')
            category_id= serializer.data.get('category_id')
            author_id= serializer.data.get('author_id')
            promote= serializer.data.get('promote')
         else:
            return Response({'message': 'Bad request!!'},status.HTTP_400_BAD_REQUEST)
         
         user = User.objects.get(id= author_id)
         author = UserProfile.objects.get(user=user)
         category= Category.objects.get(id= category_id)

         article = Article()
         article.title = title
         article.cover = cover
         article.content = content
         article.category = category
         article.author = author
         article.promote = promote
         article.save()

         return Response({'msg': 'OK'}, status.HTTP_200_OK)

      except :
         return Response({'message': 'internal server error'},status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateArticleAPIView(APIView):
   def put(self, request, format= None):
      try:
         serializer= serializers.UpdateArticleSerializer(data= request.data)
         if serializer.is_valid() :
            article_id = serializer.data.get('article_id')
            new_cover = request.FILES['cover']
         else:
            return Response({'msg': 'Bad request'},status.HTTP_400_BAD_REQUEST)
         
         Article.objects.filter(id= article_id).update(cover = f'files/article_cover/{new_cover}')
         
         return Response({'msg': 'OK'}, status.HTTP_200_OK)

      except:
         return Response({'message': 'internal server error'},status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteArticleAPIView(APIView):
   def delete(self, request, format= None):
      try:
         serializer= serializers.DeleteArticleSerializer(data= request.data)
         if serializer.is_valid() :
            article_id = serializer.data.get('article_id')
            Article.objects.filter(id= article_id).delete()
            
            return Response({'msg': 'OK'}, status.HTTP_200_OK)
      except:
         return Response({'msg': 'Bad request'},status.HTTP_400_BAD_REQUEST)




