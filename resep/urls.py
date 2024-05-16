from django.urls import path
from .views.bahan_views import *
from .views.toping_views import *
from .views.master_resep import *
from .views.utils_views import *

urlpatterns = [
    path('toping/', TopingList.as_view(), name='toping_list'),
    path('toping/create/', toping_create, name='toping_create'),
    path('toping/detail/<int:pk>/', TopingDetail.as_view(), name='toping_detail'),
    path('toping/update/<int:pk>/', TopingUpdateView.as_view(), name='toping_update'),
    path('toping/delete/<int:pk>/', TopingDelete.as_view(), name='toping_delete'),

    path('master-resep/', MasterResepList.as_view(), name='master_resep_list'),
    path('master-resep/create/', master_resep_create, name='master_resep_create'),
    path('master-resep/detail/<int:pk>/', MasterResepDetail.as_view(), name='master_resep_detail'),
    path('master-resep/update/<int:pk>/', MasterResepUpdateView.as_view(), name='master_resep_update'),
    path('master-resep/delete/<int:pk>/', MasterResepDelete.as_view(), name='master_resep_delete'),
    
    path('bahan-baku/', BahanList.as_view(), name='bahan_baku_list'),
    path('bahan-baku/<int:pk>/', BahanDetail.as_view(), name='bahan_baku_detail'),
    path('bahan-baku/create/', BahanCreate.as_view(), name='bahan_baku_create'),
    path('bahan-baku/update/<int:pk>/', BahanUpdate.as_view(), name='bahan_baku_update'),
    path('bahan-baku/delete/<int:pk>/', BahanDelete.as_view(), name='bahan_baku_delete'),

    # cek bahan, by id
    path('cek_bahan/<int:id>/', cek_bahan, name='cek_bahan'),
    path('cek_master/<int:id>/', cek_master, name='cek_master'),
    path('error/', ErrorPageView.as_view(), name='error_page'),
]
