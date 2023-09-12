"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('ckeditor/',include('ckeditor_uploader.urls')),
    path('', include('blog.urls')),
    path('auth/', include('rest_framework.urls')),

]
# if settings.DEBUG :
#     urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
#     urlpatterns += static('contact/static/', document_root= settings.STATIC_ROOT)
#     urlpatterns += static('about/static/', document_root= settings.MEDIA_ROOT)
#     urlpatterns += static('category/static/', document_root= settings.MEDIA_ROOT)



