# views.py
import json

from django.db.models.query import QuerySet
from django.views import View  
from ..models import ResepBahanJadi, MasterBahan, BarangJadi
from ..forms import BarangJadiForm, MasterBahanForm, ResepForm
# JsonResponse untuk merespons data dalam format JSON
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

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
        context['selisih'] = selisih
        return context

@login_required(login_url='login')
# Fungsi untuk mengecek detail bahan dan merespons dalam format JSON
def cek_bahan(request, id):
    # Mengambil objek bahan dari database berdasarkan id
    bahan = MasterBahan.objects.get(id=id)
    # Menyiapkan data bahan dalam format JSON
    result = {
        "kode_bahan": bahan.kode_bahan,
        "nama": bahan.nama,
        "total": bahan.total,
        "qty_keseluruhan": bahan.qty_keseluruhan,
        "qty_terkecil": bahan.qty_terkecil,
        "harga": bahan.harga,
        "harga_jual": bahan.harga_jual,
        "harga_kg": bahan.harga_kg,
        "harga_gram": bahan.harga_gram,
        "created_date": bahan.created_date,
        "updated_date": bahan.updated_date
    }
    # Mengirimkan response dalam format JSON
    return JsonResponse(result)

@login_required(login_url='login')
def cek_master(request, id):
    # Mengambil objek bahan dari database berdasarkan id
    bahan = BarangJadi.objects.get(id=id)
    print('bahan: ', bahan)
    # Menyiapkan data bahan dalam format JSON
    result = {
        'nama' : bahan.nama,
        'kode_master' : bahan.kode_barang, # Perbaiki ini menjadi kode_barang
        'harga_jual' : bahan.harga_jual,
        'daftar_bahan' : bahan.daftar_bahan,
        'hpp' : bahan.hpp,
        'is_deleted' : bahan.is_deleted,
        'master_roti' : bahan.master_roti,
    }
    # Mengirimkan response dalam format JSON
    return JsonResponse(result)


@login_required(login_url='login')
# Fungsi untuk membuat resep baru
def resep_create(request):
    # Mengambil semua bahan yang belum dihapus dari database
    bahans = MasterBahan.objects.filter(is_deleted=False)
    masters = BarangJadi.objects.filter()
    
    # Membuat form untuk input resep
    form = ResepForm(request.POST or None)

    # Jika request method adalah POST (form telah disubmit)
    if request.method == 'POST':
        # Memeriksa apakah form valid
        if form.is_valid():
            # Mengambil data dari form
            nama_roti = request.POST.get('nama_roti')
            kode_barang = request.POST.get('kode_barang')
            harga_jual = request.POST.get('harga_jual')
            hpp = request.POST.get('hpp')
            
            # Mengambil daftar id bahan dan jumlah satuan dari form
            id_bahan_list = request.POST.getlist('id_bahan[]')
            jumlah_satuan_list = request.POST.getlist('jumlah_satuan[]')
            
            # Simpan data resep ke dalam database
            barang_jadi = BarangJadi.objects.create(
                nama=nama_roti,
                kode_barang=kode_barang,
                harga_jual=harga_jual,
                hpp=hpp,
            )
            
            # Membuat daftar bahan yang akan disimpan dalam bentuk JSON
            daftar_bahan = []
            for i in range(len(id_bahan_list)):
                # Mengambil objek bahan dari database berdasarkan id
                bahan_id = id_bahan_list[i]
                bahan_obj = MasterBahan.objects.get(id=bahan_id)
                
                # Membuat dictionary untuk setiap bahan
                
                """ Mekanisme Kurang bersih
                bahan = {
                    'id_bahan': bahan_id,
                    'nama_bahan': bahan_obj.nama,
                    'kode_bahan': bahan_obj.kode_bahan,
                    'harga_jual': harga_jual,
                    'jumlah_satuan': jumlah_satuan_list[i],
                }
                daftar_bahan.append(bahan)
                """
                # Simpan data resep ke dalam database
                resep_create = ResepBahanJadi.objects.create(
                    master_bahan = bahan_obj,
                    barang_jadi  = barang_jadi, 
                    jumlah_pemakaian = jumlah_satuan_list[i],
                )
                
            """ Mekanisme Kurang bersih 
            daftar_bahan_json = json.dumps(daftar_bahan)
            barang_jadi.daftar_bahan = daftar_bahan_json
            barang_jadi.save()
            """
            # Redirect ke halaman detail resep
            return redirect('resep_detail', pk=barang_jadi.id)

    # Mengirimkan data bahan dan form ke template
    context = {'bahans': bahans, 'form': form}
    return render(request, 'resep/resep_form.html', locals())


class ResepUpdateView(LoginRequiredMixin,  UpdateView):
    model = BarangJadi
    form_class = BarangJadiForm
    template_name = 'resep/resep_update.html'
    success_url = '/'
    context_object_name = 'barang_jadi'
    login_url = 'login'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        barang_jadi = self.object
        print('barang_jadi: ', barang_jadi)
        
        daftar_resep = ResepBahanJadi.objects.filter(barang_jadi=barang_jadi)
        print('daftar_resep: ', daftar_resep)
        context['daftar_resep'] = daftar_resep
        context['bahans'] = MasterBahan.objects.filter(is_deleted=False)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        nama_roti = self.request.POST.get('nama_roti')
        kode_barang = form.cleaned_data.get('kode_barang')
        harga_jual = form.cleaned_data.get('harga_jual')
        hpp = form.cleaned_data.get('hpp')
        
        # Update data barang jadi
        self.object.nama = nama_roti
        self.object.kode_barang = kode_barang
        self.object.harga_jual = harga_jual
        self.object.hpp = hpp
        self.object.save()

        # Delete existing resep
        ResepBahanJadi.objects.filter(barang_jadi=self.object).delete()

        # Simpan data resep ke dalam database
        for i in range(len(self.request.POST.getlist('id_bahan[]'))):
            bahan_id = self.request.POST.getlist('id_bahan[]')[i]
            bahan_obj = MasterBahan.objects.get(id=bahan_id)
            jumlah_pemakaian = self.request.POST.getlist('jumlah_satuan[]')[i]
            ResepBahanJadi.objects.create(
                master_bahan=bahan_obj,
                barang_jadi=self.object,
                jumlah_pemakaian=jumlah_pemakaian,
            )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('resep_detail', kwargs={'pk': self.object.id})