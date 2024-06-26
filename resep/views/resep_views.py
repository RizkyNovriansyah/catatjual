# views.py
import json

from ..models import ResepBahanJadi, MasterBahan, BarangJadi,BahanOlahan,ResepOlahanJadi
from ..forms import BarangJadiForm
from .utils_views import add_resep_to_jadi, get_bahan_used, get_olahan_used
# JsonResponse untuk merespons data dalam format JSON
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
# from import reserve 
from django.urls import reverse

# Kelas untuk menampilkan daftar resep.
class ResepList(LoginRequiredMixin, ListView):
    # Menentukan model yang akan digunakan untuk menampilkan daftar.
    model = BarangJadi
    # Menentukan nama template yang akan digunakan untuk render halaman.
    template_name = 'resep/resep_list.html'
    # Menentukan nama objek konteks yang akan digunakan di template.
    context_object_name = 'barang_jadis'
    login_url = 'login'
    
    def get_queryset(self):
        return BarangJadi.objects.filter(is_deleted=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
            
# Kelas untuk menghapus data resep.
class ResepDelete(LoginRequiredMixin, DeleteView):
    # Menentukan model yang akan dihapus.
    model = BarangJadi
    # Menentukan nama objek konteks yang akan digunakan di template.
    context_object_name = 'barang_jadi'
    # Menentukan URL yang akan diarahkan setelah proses penghapusan berhasil.
    success_url = reverse_lazy('resep_list')
    login_url = 'login'

# Kelas untuk menampilkan detail resep.
class ResepDetail(LoginRequiredMixin, DetailView):
    # Menentukan model yang akan ditampilkan detailnya.
    model = BarangJadi
    # Menentukan nama template yang akan digunakan untuk render halaman.
    template_name = 'resep/resep_detail.html'
    # Menentukan nama objek konteks yang akan digunakan di template.
    context_object_name = 'barang_jadi'   
    login_url = 'login'
    
    # Method untuk mendapatkan data bahan yang digunakan dalam resep.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Menghitung selisih antara harga jual dan harga pokok penjualan.
        selisih = self.object.harga_jual - self.object.hpp
        # Mendapatkan id resep.
        id_bahan = self.object.id
        # Mendapatkan daftar bahan yang digunakan dalam resep.
        resep = ResepBahanJadi.objects.filter(barang_jadi__id=id_bahan)
        
        bahans = []
        # Loop untuk setiap bahan dalam resep.
        for bahan in resep:
            nama = bahan.master_bahan.nama
            jumlah = bahan.jumlah_pemakaian
            # Menghitung total harga pokok penjualan untuk satu bahan.
            total_hpp_single_bahan = bahan.master_bahan.harga_gram * jumlah
            bahans.append({'nama' : nama, 
                           'jumlah' : jumlah,
                           'kode_bahan' : bahan.master_bahan.kode_bahan,
                           'harga_gram': bahan.master_bahan.harga_gram,
                           'total_hpp_single_bahan' : total_hpp_single_bahan,
                           })
            
        # Menyimpan daftar bahan dan selisih ke dalam konteks.
        context['bahans'] = bahans

        resepOlahan = ResepOlahanJadi.objects.filter(barang_jadi__id=id_bahan)
        olahans = []
        for olahan in resepOlahan:
            nama = olahan.bahan_olahan.nama
            jumlah = olahan.jumlah_pemakaian
            total_hpp_single_bahan = olahan.bahan_olahan.harga_gram * jumlah
            olahans.append({'nama' : nama, 
                           'jumlah' : jumlah,
                           'kode_bahan' : "olahan_"+str(olahan.bahan_olahan.id),
                           'harga_gram': olahan.bahan_olahan.harga_gram,
                           'total_hpp_single_bahan' : total_hpp_single_bahan,
                           })
        
        context['olahans'] = olahans
        context['selisih'] = selisih
        return context

# Fungsi untuk membuat resep baru
class ResepCreate(LoginRequiredMixin, CreateView):
    model = BarangJadi
    form_class = BarangJadiForm
    template_name = 'resep/resep_form.html'
    success_url = reverse_lazy('bahan_olah_list')
    login_url = 'login'

    def get_success_url(self):
        return reverse_lazy('resep_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        list_bahans = json.loads(self.request.POST.get('list_bahans'))
        form.instance.save()
        add_resep_to_jadi(form.instance, list_bahans)

        return super(ResepCreate,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bahans'] = MasterBahan.objects.filter(is_deleted=False)
        context['olahans'] = BahanOlahan.objects.filter(is_deleted=False)
        context['url_get_bahan'] = reverse('cek_bahan', kwargs={'id': 99999})
        context['url_get_olahan'] = reverse('cek_bahan_olah', kwargs={'id': 99999})
        context['olahan_used'] = []
        context['bahan_used'] = []

        return context


class ResepUpdateView(LoginRequiredMixin,  UpdateView):
    model = BarangJadi
    form_class = BarangJadiForm
    template_name = 'resep/resep_form.html'
    login_url = 'login'

    def get_success_url(self):
        return reverse_lazy('resep_detail', kwargs={'pk': self.object.id})
    
    def get_context_data(self, **kwargs):
        barang_jadi = self.object
        context = super().get_context_data(**kwargs)
        context['bahans'] = MasterBahan.objects.filter(is_deleted=False)
        context['olahans'] = BahanOlahan.objects.filter(is_deleted=False)
        context['url_get_bahan'] = reverse('cek_bahan', kwargs={'id': 99999})
        context['url_get_olahan'] = reverse('cek_bahan_olah', kwargs={'id': 99999})
        context['bahan_used'] = get_bahan_used(barang_jadi)
        context['olahan_used'] = get_olahan_used(barang_jadi)
        
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)

        list_bahans = json.loads(self.request.POST.get('list_bahans'))
        ResepBahanJadi.objects.filter(barang_jadi=self.object).delete()
        ResepOlahanJadi.objects.filter(barang_jadi=self.object).delete()
        add_resep_to_jadi(form.instance, list_bahans)

        return super().form_valid(form)