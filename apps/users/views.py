from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from apps.users.models import User


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


   


def user_login (request):
   if request.user.is_authenticated :
      return redirect("blog:home-blog")

   if request.method == "POST":
      if "submit" in request.POST:
      
         username = request.POST["username"]
         password = request.POST["password"]
         user = authenticate(request, username=username, password=password)
         print( user)
         if user is not None:
            login(request, user)
            return redirect("blog:home-blog")
         else:
            messages.success(request, ("invalid username or password"))
            return redirect("users:user-login")
            
   else:
      return render(request, 'users/login.html', context={})


def user_logout (request):
   logout(request)
   return redirect("blog:home-blog")