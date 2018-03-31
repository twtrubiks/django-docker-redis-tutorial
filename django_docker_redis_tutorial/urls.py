"""django_docker_redis_tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from musics.views import MusicViewSet

router = DefaultRouter()
router.register(r'music', MusicViewSet, base_name='music')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('images/', include('images.urls')),
]

# issue ref. https://github.com/encode/django-rest-framework/pull/5609
urlpatterns += [
    url(r'^api/', include((router.urls, 'rest_framework'), namespace='api')),
]
