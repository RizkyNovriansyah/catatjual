# views.py
import json

from django.views import View  
from ..models import Resep, MasterBahan, BarangJadi
from ..forms import BarangJadiForm, MasterBahanForm, ResepForm
# JsonResponse untuk merespons data dalam format JSON
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView


#Bahan
class BahanCreate(CreateView):
    # Menentukan model yang digunakan untuk membuat objek.
    model = MasterBahan
    # Menentukan form class yang digunakan untuk membuat form.
    form_class = MasterBahanForm
    # Menentukan URL yang akan diarahkan setelah pembuatan objek berhasil.
    success_url = reverse_lazy('bahan_list')
    
    # Override method form_valid untuk memproses form yang valid.
    def form_valid(self, form):
        # Mendapatkan nilai harga dari form.
        harga = form.cleaned_data['harga']
        # Mendapatkan nilai quantity keseluruhan dari form.
        quantity = form.cleaned_data['qty_keseluruhan']
        # Mendapatkan nilai quantity terkecil dari form.
        quantity_terkecil = form.cleaned_data['qty_terkecil']
        
        # Menghitung harga per kilogram jika quantity tidak sama dengan 0.
        if quantity != 0:
            harga_kg = harga / quantity
            # Menghitung harga per gram berdasarkan harga per kilogram.
            harga_gram = harga_kg / quantity_terkecil
        else:
            # Jika quantity sama dengan 0, set harga per kilogram dan harga per gram menjadi 0.
            harga_kg = 0
            harga_gram = 0
        
        # Menyimpan nilai harga per kilogram dan harga per gram ke instance form.
        form.instance.harga_kg = harga_kg
        form.instance.harga_gram = harga_gram
        
        # Memanggil method form_valid dari superclass untuk melanjutkan proses validasi form.
        return super(BahanCreate, self).form_valid(form)
    
# Kelas untuk menampilkan daftar bahan.
class BahanList(ListView):
    # Menentukan model yang akan digunakan untuk menampilkan daftar.
    model = MasterBahan
    # Menentukan nama template yang akan digunakan untuk render halaman.
    template_name = 'resep/masterbahan_list.html'
    # Menentukan nama objek konteks yang akan digunakan di template.
    context_object_name = 'bahans'

# Kelas untuk mengupdate data bahan.
class BahanUpdate(UpdateView):
    # Menentukan model yang akan diupdate.
    model = MasterBahan
    # Menentukan fields yang bisa diubah pada proses update.
    fields = ['kode_bahan', 'nama', 'total', 'qty_keseluruhan', 'qty_terkecil', 'harga', 'harga_jual']
    # Menentukan URL yang akan diarahkan setelah proses update berhasil.
    success_url = reverse_lazy('bahan_list')
    
# Kelas untuk menghapus data bahan.
class BahanDelete(DeleteView):
    # Menentukan model yang akan dihapus.
    model = MasterBahan
    # Menentukan nama objek konteks yang akan digunakan di template.
    context_object_name = 'bahan'
    # Menentukan URL yang akan diarahkan setelah proses penghapusan berhasil.
    success_url = reverse_lazy('bahan_list')

# Kelas untuk menampilkan detail bahan.
class BahanDetail(DetailView):
    # Menentukan model yang akan ditampilkan detailnya.
    model = MasterBahan
    # Menentukan nama template yang akan digunakan untuk render halaman.
    template_name = 'resep/masterbahan_detail.html'
    # Menentukan nama objek konteks yang akan digunakan di template.
    context_object_name = 'bahan'
    