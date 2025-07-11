"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('users/', include('users.urls', namespace='users')),
    path('curation/', include('submission.urls', namespace='submission')),
    path('catalog/', include('catalog.urls', namespace='catalog')),
    path('inventory/', include('inventory.urls', namespace='inventory')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('pages.urls')),

    
]

# Apenas em modo de desenvolvimento, sirva os arquivos de mídia localmente
if settings.DEBUG:
    # Adiciona as URLs para os arquivos estáticos
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # Adiciona as URLs para os arquivos de mídia
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)