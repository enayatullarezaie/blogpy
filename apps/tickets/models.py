from django.db import models




class Ticket(models.Model):
   title= models.TextField(max_length=256)
   body= models.CharField(max_length= 64)
   created_at= models.DateTimeField(auto_now_add=True)


