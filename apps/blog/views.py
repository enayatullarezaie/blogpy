from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import TemplateView, RedirectView, View, ListView, DetailView, CreateView,FormView, UpdateView, DeleteView
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from django.core.paginator import Paginator
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin



class LikeHandler(TemplateView):
   def get(self, request):
      return JsonResponse({ "detail" : "detail" })

   def post(self, request):
      article_id = request.POST['article_id']
      user = request.user.id
      try:
         like = Like.objects.filter(article_id= article_id, user_id=user).first()
         if like:
            like.delete()
            like_by_me  = False
         else:
            like = Like.objects.create(article_id= article_id, user_id= request.user.id)
            like_by_me  = True
         return JsonResponse({ "like_by_me": like_by_me })
      except Exception as err:
         print(err)
         return HttpResponse({}, status=400)
         

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


class IndexPage(View):
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
      # self.request.session["name"] = "enayat"
      print(self.request.session["name"])
      return render(request, "blog/index.html", context)
   

      
class ArticleDetailView(DetailView):
   model= Article
   template_name= 'blog/article_detail'
   context_object_name= ('article', 'object',)
   

class ArticleFormView(FormView):
   form_class = TicketForm
   template_name= 'blog/article_form'
   success_url= reverse_lazy("blog:home")

   def form_valid(self, form) -> HttpResponse:
      data = form.cleaned_data
      Ticket.objects.create(**data)
      return super().form_valid(form)
   
   def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
      context = super().get_context_data(**kwargs)
      context["tickets"] = Ticket.objects.all()
      return context
   

class ArticleCreateView(CreateView):   
   model= Article
   template_name= 'blog/article_form'
   success_url= reverse_lazy("blog:home")

   def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
      context = super().get_context_data(**kwargs)
      context["articles"] = Article.objects.all()
      return context                     
   
   def form_valid(self, form: BaseModelForm) -> HttpResponse:
      instance = form.save(commit=False)
      instance.email = self.request.user.email
      instance.save()
      return super().form_valid(form)
   
   def get_success_url(self) -> str:
      print(self.object)
      return super(ArticleCreateView, self).get_success_url()


class ArticleUpdateView(UpdateView):
   model= Article
   fields= '__all__'
   template_name= 'blog/article_update_form'
   success_url = '/'


class ArticleDeleteView(DeleteView):
   model= Article
   success_url = '/'


class ArticleDetail(TemplateView):
   def get(self, request, slug):
      try:
         if request.user.likes.filter(article__slug = slug ):
            like_by_me = True
         else:
            like_by_me= False
            
         article= Article.objects.get(slug= slug)
      except:
         return HttpResponse({}, status=404)
      
      context={
         "article": article, 
         'like_by_me': like_by_me,
      }
      return render( request,'blog/article_detail.html', context=context)
   
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
      
      if request.user.likes.filter(article__slug = slug ):
         like_by_me = True
      else:
         like_by_me= False
         
      new_comm = Comment.objects.create(
         user= user,
         text = text,
         article = article,
         like_by_me = like_by_me
      )
      context={ 
         "article": article, 
      }
      

         
      return render( request,'blog/article_detail.html', context=context)


class ContactPage(TemplateView):
   def get(self, request):
      form = ContactForms()
      form = TicketForm()

      return render(request, 'blog/contact-page.html', context={"form": form})
   
   def post(self, request):
      form =  ContactForms(data= request.POST)
      if form.is_valid():
         fullname =  form.cleaned_data.get("fullname")
         title =  form.cleaned_data.get("title")
         text =  form.cleaned_data.get("text")
         print(fullname, title, text)

      return render(request, 'blog/contact-page.html', context={"form": form})


class AboutPage(TemplateView):
   template_name = 'blog/page-about.html'
   def get_context_data(self, **kwargs: Any):
      context= super().get_context_data(**kwargs)
      context['object_list'] = Article.objects.all()
      return context


class CategoryPage(TemplateView):
   def get (self, request):
      return render(request, 'blog/category-page.html', context={})


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




