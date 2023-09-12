from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers



class IndexPage(TemplateView):

   def get(self, request, **kwargs):
      article_data = []
      all_articles = Article.objects.order_by('-created_at').all()[:]

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

class AboutPage(TemplateView):
   template_name = 'page-about.html'

class CategoryPage(TemplateView):
   template_name = 'category.html'


class AllArticlesAPIView(APIView):

   def get(self, request):
      try:
         all_articles = Article.objects.order_by('-created_at').all()
         data= []
         for article in all_articles :
            data.append({
               "id": article.id,
               "title": article.title,
               "cover": article.cover.url if article.cover else None,
               "content": article.content,
               "category": article.category.title,
               "author": article.author.user.first_name + ' ' + article.author.user.last_name,
               "created_at": article.created_at.date(),
               "promote": article.promote,
            })
         return Response({ "data": data }, status.HTTP_200_OK)
      except:
         return Response({'message': 'Internal Server Error'},status.HTTP_500_INTERNAL_SERVER_ERROR)
      

class SingleArticleAPIView(APIView):
   def get(self, request, format=None):
      try:
         article_title = request.GET['article_title']
         article = Article.objects.filter(title__contains= article_title)
         serialized_data = serializers.SingleArticleSerializer(article, many= True)
         data = serialized_data.data

         return Response({"data":data}, status.HTTP_200_OK)

      except:
         return Response({'message': 'internal server error'},status.HTTP_500_INTERNAL_SERVER_ERROR)


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
         
         Article.objects.filter(id= article_id).update(cover = f'article_cover/{new_cover}')
         
         return Response({'msg': 'OK'}, status.HTTP_200_OK)

      except:
         return Response({'message': 'internal server error'},status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteArticleAPIView(APIView):
   def delete(self, request, format= None):
      try:
         serializer= serializers.DeleteArticleSerializer(data= request.data)
         if serializer.is_valid() :
            article_id = serializer.data.get('article_id')
         else:
            return Response({'msg': 'Bad request'},status.HTTP_400_BAD_REQUEST)
         
         Article.objects.filter(id= article_id).delete()
         
         return Response({'msg': 'OK'}, status.HTTP_200_OK)

      except:
         return Response({'message': 'internal server error'},status.HTTP_500_INTERNAL_SERVER_ERROR)




