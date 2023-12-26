from django.shortcuts import render
from .models import *
# Create your views here.


def gethome(request):

   if request.method =="POST":
      if "save" in request.POST:
         Message.objects.create(
            fullname= request.POST.get("fullname"),
            email= request.POST.get("email"),
            title= request.POST.get("title"),
            body= request.POST.get("body"),
         )
         
   samples =Project.objects.all()[:6]
   return render(request, 'home/index.html', context={"samples":samples})



