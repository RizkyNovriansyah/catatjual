from django.urls import path
from .views import *

urlpatterns = [
    path('pesanan/', PesananListView.as_view(), name='pesanan_list'),
    path('pesanan/create/', PesananCreate.as_view(), name='pesanan_create'),
    path('pesanan/<int:pk>/', PesananDetailView.as_view(), name='pesanan_detail'),
    path('pesanan/<int:pk>/update/', PesananUpdate, name='pesanan_update'),
    path('pesanan/<int:pk>/delete/', PesananDelete, name='pesanan_delete'),
    
    
    path('cek_pesanan/<int:id>/', cek_pesanan, name='cek_pesanan'),
    
]
