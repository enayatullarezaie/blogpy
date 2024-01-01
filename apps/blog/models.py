from django.db import models
from django.urls import reverse
from apps.users.models import User
from datetime import datetime
from django.utils.text import slugify
from django.utils.html import format_html

def validate_file_extension (value):
   import os
   from django.core.exceptions import ValidationError
   ext = os.path.splitext(value.name)[1]
   valid_extensions = ['.jpeg', '.jpg', '.png', '.webp'] 
   if not ext.lower() in valid_extensions:
      raise ValidationError('Unsupported file extension.')


class UserProfile (models.Model) :
   id = models.BigAutoField(primary_key= True, editable=False)
   user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
   avatar = models.FileField(upload_to= 'images/user_avatar/', null=False, blank=False, validators= [validate_file_extension])
   description = models.CharField(max_length=512, null=False, blank=False)
   def __str__(self):
      return self.user.username


class Category (models.Model):
   title = models.CharField(max_length=128, null=False, blank=False)
   cover = models.FileField(
      upload_to='images/category_cover/', 
      null=False, 
      blank= False, 
      validators= [validate_file_extension] 
   )
   objects = models.Manager()
   def __str__(self):
      return self.title



class Article(models.Model):
   id = models.BigAutoField(primary_key= True, editable=False)
   title = models.CharField(max_length=256, null=False, blank=False, unique= True)
   slug = models.SlugField(max_length=256, null=True, blank=True, unique= True, allow_unicode=True)
   content = models.TextField(max_length=5120)
   category = models.ForeignKey(Category, on_delete= models.CASCADE)
   author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
   promote= models.BooleanField(default= False)
   created_at = models.DateTimeField(auto_now_add=True, blank=False)
   updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
   cover = models.FileField (
      upload_to='images/article_cover/', 
      null=False, 
      blank=False, 
      validators= [validate_file_extension]
   )
   objects = models.Manager()
   class Meta:
      ordering= ('-created_at',)

   def get_absolute_url(self):
      return reverse('blog:detail', kwargs= {"slug": self.slug})
   
   def get_cover(self):
      if self.cover:
         return format_html(
            f"<img src='{self.cover.url}' width='50px' height='40px' style='object-fit:cover'>"
         )
      else:
         return format_html("<h4>no cover</h4>")
   def save(self) -> None:
      self.slug = self.title.replace(" ", "-")
      self.slug = slugify(self.title, allow_unicode=True)

      print(slugify(self.title, allow_unicode=True))
      super(Article, self).save()
   
   def __str__(self):
      return self.title


class Comment(models.Model):
   article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True, related_name= "comments")
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "comments")
   parent = models.ForeignKey("Comment" , on_delete=models.CASCADE, null=True, blank=True, related_name= "replies")
   text = models.TextField(max_length=256,null =True)
   created_at = models.DateTimeField(auto_now_add=True)
   class Meta:
      ordering= ['-created_at']
   def __str__(self) -> str:
      return self.article.title


class Like(models.Model):
   id = models.BigAutoField(primary_key= True, editable=False)
   user = models.ForeignKey(User, on_delete= models.CASCADE, null=True, related_name= "likes")
   article = models.ForeignKey(Article, on_delete= models.CASCADE, null=True, related_name= "likes")
   created_at= models.DateTimeField(auto_now_add=True, null=True)


class DisLike(models.Model):
   id = models.BigAutoField(primary_key= True, editable=False)
   user = models.ForeignKey(User, on_delete= models.CASCADE, null=True, related_name= "dislikes")
   article = models.ForeignKey(Article, on_delete= models.CASCADE, null=True, related_name= "dislikes")
   created_at= models.DateTimeField(auto_now_add=True, null=True)


