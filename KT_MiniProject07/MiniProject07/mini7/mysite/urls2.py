"""
URL configuration for mysite project.

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
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

def index(request):
    return render(request,'index.html')

def signup(request):
    return render(request,'signup.html')

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('chatgpt/',include('chatgpt.urls')),
    path('signlanguagetochatgpt/',include('signlanguagetochatgpt.urls')),
    path('selfchatgpt/', include('selfchatgpt.urls')),
    path('selfsignlanguagetochatgpt/', include('selfsignlanguagetochatgpt.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', index),
    path('accounts/', include('accounts.urls'), name='accounts'),    
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)