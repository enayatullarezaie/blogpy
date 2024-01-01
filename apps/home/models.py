from django.db import models


class Project(models.Model):
   title= models.CharField(max_length= 128)
   description= models.TextField(max_length= 256)
   customer= models.CharField(max_length= 128)
   team= models.CharField(max_length= 128)
   cover= models.ImageField(upload_to= 'images/project_cover/')
   created_at= models.DateTimeField(auto_now_add=True)



class Message(models.Model):
   fullname= models.CharField(max_length= 128)
   email= models.EmailField(null=True)
   title= models.CharField(max_length= 128)
   body= models.TextField(max_length= 256)
   created_at= models.DateTimeField(auto_now_add=True)




   