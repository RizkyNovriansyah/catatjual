# urls.py
from django.urls import path
from .views.bahan_views import *
from .views.resep_views import *
from .views.master_resep import *

urlpatterns = [
    path('', ResepList.as_view(), name='resep_list'),
    path('create/', resep_create, name='resep_create'),
    path('update/<int:pk>/', ResepUpdateView.as_view(), name='resep_update'),
    path('delete/<int:pk>/', ResepDelete.as_view(), name='resep_delete'),
    path('detail/<int:pk>/', ResepDetail.as_view(), name='resep_detail'),
    
    
    path('bahans/', BahanList.as_view(), name='bahan_list'),
    path('bahans/<int:pk>/', BahanDetail.as_view(), name='bahan_detail'),
    path('bahans/create/', BahanCreate.as_view(), name='bahan_create'),
    path('bahans/update/<int:pk>/', BahanUpdate.as_view(), name='bahan_update'),
    path('bahans/delete/<int:pk>/', BahanDelete.as_view(), name='bahan_delete'),

    # cek bahan, by id
    path('cek_bahan/<int:id>/', cek_bahan, name='cek_bahan'),

]
