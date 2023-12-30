from django.shortcuts import render, HttpResponse, redirect
from .models import *
from apps.courses.forms import CourseForm


def root(request):
   courses = Course.objects.all()
   return render(request, 'courses/index.html', context={"courses": courses})   


def get_cource_detail(request, pk):

   course = Course.objects.get(id = pk) 
   course.views += 1
   course.save()
   return render(request, 'courses/detail.html', context={"detail": course})


def new_cource(request):
   form = CourseForm()

   if request.method == "POST":

      title= request.POST.get("title")
      description= request.POST.get("description")
      cover= request.POST.get("cover")

      if title and description and cover :
         course = Course.objects.create(
            title= title, 
            description =description, 
            cover=cover
         )
         # course.save()
         return redirect("/courses/")
   
   if request.method == "POST":
      submitted = False
      if 'save' in request.POST :
         form = CourseForm(request.POST, request.FILES)
         if form.is_valid():
            course= form.save(commit=False)
            # course.owner = request.user.id
            course.save()
            # form.save()
         return redirect("/courses/")
   
   return render(request, 'courses/new-course.html', context={ "form": form})
