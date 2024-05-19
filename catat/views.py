from django.shortcuts import render
import json
from django.db.models.query import QuerySet
from django.views import View  
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from resep.models import BarangJadi, MasterBahan, Resep
from pesan.models import ListPesanan, Pesanan


def dashboard(request):
    barang_jadi_count = BarangJadi.objects.filter(is_deleted=False).count()
    resep_count = Resep.objects.filter(is_deleted=False).count()
    bahan_count = MasterBahan.objects.filter(is_deleted=False).count()
    list_pesanan_count = ListPesanan.objects.filter(is_deleted=False).count()
    context = {'bahan_count': bahan_count,
               'resep_count': resep_count,
               'list_pesanan_count': list_pesanan_count,
               'barang_jadi_count': barang_jadi_count}
    return render(request, 'catat/dashboard.html', context)
