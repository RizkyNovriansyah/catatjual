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

    # path('tambah_roti/', views.tambah_roti, name='tambah_roti'),
    # path('daftar_roti/', views.daftar_roti, name='daftar_roti'),
    # path('tambah_penjualan/', views.tambah_penjualan, name='tambah_penjualan'),
    # path('daftar_penjualan/', views.daftar_penjualan, name='daftar_penjualan'),
    # path('tambah_bahan_baku/', views.tambah_bahan_baku, name='tambah_bahan_baku'),
    # path('daftar_bahan_baku/', views.daftar_bahan_baku, name='daftar_bahan_baku'),
]
