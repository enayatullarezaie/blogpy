from django.contrib import admin
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
   list_display= ['user', 'avatar', 'description']
admin.site.register(UserProfile, UserProfileAdmin)

class UserLikeAdmin(admin.ModelAdmin):
   list_display= ['user', 'article']
admin.site.register(Like, UserLikeAdmin)

class UserDisLikeAdmin(admin.ModelAdmin):
   list_display= ['user', 'article']
admin.site.register(DisLike, UserDisLikeAdmin)


class CommentInline(admin.TabularInline):
   model= Comment

class ArticleAdmin(admin.ModelAdmin):
   search_fields= ['title', 'content']
   list_display= ['title', 'category', 'created_at',"promote", "get_cover"]
   list_filter = ["created_at"]
   list_editable = ["promote"]
   inlines = [CommentInline]
admin.site.register(Article, ArticleAdmin)

class CategoryAdmin(admin.ModelAdmin):
   list_display= ['title', 'cover']
admin.site.register(Category, CategoryAdmin)

class CommentAdmin(admin.ModelAdmin):
   list_display= ['article', 'user', "parent"]
admin.site.register(Comment, CommentAdmin)



