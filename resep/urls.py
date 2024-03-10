# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ResepList.as_view(), name='resep_list'),
    path('create/', views.resep_create, name='resep_create'),
    path('update/<int:pk>/', views.ResepUpdate.as_view(), name='resep_update'),
    path('delete/<int:pk>/', views.ResepDelete.as_view(), name='resep_delete'),
    path('detail/<int:pk>/', views.ResepDetail.as_view(), name='resep_detail'),
    
    path('bahans/', views.BahanList.as_view(), name='bahan_list'),
    path('bahans/<int:pk>/', views.BahanDetail.as_view(), name='bahan_detail'),
    path('bahans/create/', views.BahanCreate.as_view(), name='bahan_create'),
    path('bahans/update/<int:pk>/', views.BahanUpdate.as_view(), name='bahan_update'),
    path('bahans/delete/<int:pk>/', views.BahanDelete.as_view(), name='bahan_delete'),
]
