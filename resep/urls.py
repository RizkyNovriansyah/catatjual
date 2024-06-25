from django.urls import path
from .views.bahan_views import *
from .views.bahan_olah_views import *
from .views.resep_views import *
from .views.master_resep import *
from .views.utils_views import *

urlpatterns = [
    path('resep/', ResepList.as_view(), name='resep_list'),
    path('resep/create/', resep_create, name='resep_create'),
    path('resep/detail/<int:pk>/', ResepDetail.as_view(), name='resep_detail'),
    path('resep/update/<int:pk>/', ResepUpdateView.as_view(), name='resep_update'),
    path('resep/delete/<int:pk>/', ResepDelete.as_view(), name='resep_delete'),

    path('master_resep/', MasterResepList.as_view(), name='master_resep_list'),
    path('master_resep/create/', MasterResepCreate.as_view(), name='master_resep_create'),
    path('master_resep/detail/<int:pk>/', MasterResepDetail.as_view(), name='master_resep_detail'),
    path('master_resep/update/<int:pk>/', MasterResepUpdateView.as_view(), name='master_resep_update'),
    path('master_resep/delete/<int:pk>/', MasterResepDelete.as_view(), name='master_resep_delete'),
    
    path('bahans/', BahanList.as_view(), name='bahan_list'),
    path('bahans/<int:pk>/', BahanDetail.as_view(), name='bahan_detail'),
    path('bahans/create/', BahanCreate.as_view(), name='bahan_create'),
    path('bahans/update/<int:pk>/', BahanUpdate.as_view(), name='bahan_update'),
    path('bahans/delete/<int:pk>/', BahanDelete.as_view(), name='bahan_delete'),

    #Bahan Olah
    path('bahans_olah/', BahanOlahList.as_view(), name='bahan_olah_list'),
    path('bahans_olah/<int:pk>/', BahanOlahDetail.as_view(), name='bahan_olah_detail'),
    path('bahans_olah/create/', BahanOlahCreate.as_view(), name='bahan_olah_create'),
    path('bahans_olah/update/<int:pk>/', BahanOlahUpdate.as_view(), name='bahan_olah_update'),
    path('bahans_olah/delete/<int:pk>/', BahanOlahDelete.as_view(), name='bahan_olah_delete'),

    # cek bahan, by id
    path('cek_bahan/<int:id>/', cek_bahan, name='cek_bahan'),
    path('cek_bahan_olah/<int:id>/', cek_bahan_olah, name='cek_bahan_olah'),
    path('cek_master/<int:id>/', cek_master, name='cek_master'),
    path('error/', ErrorPageView.as_view(), name='error_page'),
]
