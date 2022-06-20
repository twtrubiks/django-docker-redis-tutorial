from django.urls import path

from . import views

urlpatterns = [
    # ex: /images/
    path('', views.index, name='index'),
    # ex: /images/5/
    path('<int:image_id>/', views.detail, name='detail'),

]