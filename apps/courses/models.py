from django.db import models
from datetime import datetime
# Create your models here.

class Course(models.Model):
   title= models.CharField(max_length= 128, null= True)
   description= models.TextField(max_length= 256, null= True)
   situation= models.BooleanField(default= True)
   views= models.IntegerField(default= 0)
   cover= models.ImageField(upload_to="courses/cover/", null=True ,default=None, blank=True)
   created_at= models.DateTimeField(auto_now_add=True)