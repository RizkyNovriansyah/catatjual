# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.resep_list, name='resep_list'),
    path('<int:pk>/', views.resep_detail, name='resep_detail'),
    path('create/', views.resep_create, name='resep_create'),
    path('bahans/', views.bahan_list, name='bahan_list'),
    path('bahans/<int:pk>/', views.bahan_detail, name='bahan_detail'),
    path('bahans/create/', views.bahan_create, name='bahan_create'),
]
