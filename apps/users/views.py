from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from apps.users.models import User
from django.views.generic import TemplateView 
from .forms import *




class UserRegisterView(TemplateView):
   def post(self, request):
      if request.user.is_authenticated :
         return redirect("blog:home-blog")
      
      form = UserCreationForm(request.POST)
      print("BEFORE is_valid()")
      if form.is_valid():
         print("AFTER is_valid()")
         print("BEFOR form.save()")
         user = form.save()
         login(request, user)
         print("AFTER form.save()")
         return redirect("blog:home-blog")
         
      return render(request, 'users/register.html', context={"form": form})
   
   def get(self, request):
      if request.user.is_authenticated :
         return redirect("blog:home-blog")
      
      form = UserCreationForm()
      
      return render(request, 'users/register.html', context={"form": form})
      
      
def user_register (request):
   if request.user.is_authenticated :
      return redirect("blog:home-blog")
   
   if request.method == "POST":
      username = request.POST["username"]
      password = request.POST["password"]
      user = User.objects.create( username=username, password=password)
      if user :
         login(request, user)
         return redirect("blog:home-blog")
      else:
         messages.success(request, ("invalid username or password"))
         return redirect("users:user-register")
         
   else:
      return render(request, 'users/register.html', context={})


class UserLogin(TemplateView):
   def get(self, request):
      if request.user.is_authenticated :
            return redirect("blog:home-blog")
      
      return render(request, 'users/login.html', context={})
   
   def post(self, request):
      if request.user.is_authenticated :
            return redirect("blog:home-blog")
      
      if "submit" in request.POST:
         username = request.POST["username"]
         password = request.POST["password"]
         user = authenticate(request, username=username, password=password)

         if user is not None:
            login(request, user)
            return redirect("blog:home-blog")
         else:
            messages.success(request, ("invalid username or password"))
            return redirect("users:user-login")
      
      return render(request, 'users/login.html', context={})


def user_logout (request):
   logout(request)
   return redirect("blog:home-blog")


class UserEdit(TemplateView):
   def get(self, request):
      if not request.user.is_authenticated :
            return redirect("users:user-login")
      form = UserEditForm(instance= request.user)
      
      return render(request, 'users/edit.html', context={"form": form})
   
   def post(self, request):
      if not request.user.is_authenticated :
            return redirect("users:user-login")
      
      form = UserEditForm(instance=request.user, data=request.POST)
      if form.is_valid():
         form.save()
      
      return render(request, 'users/edit.html', context={"form": form})

