from apps.blog.models import Article





def recent_articles(request):
   recent_arts =  Article.objects.all().order_by("-created_at")

   return {"recent_arts": recent_arts}