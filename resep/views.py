# views.py
from .models import Resep, MasterBahan, BarangJadi
from .forms import MasterBahanForm, ResepForm
from django.db.models import Sum

import json  
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

#Bahan
class BahanCreate(CreateView):
    model = MasterBahan
    form_class = MasterBahanForm
    success_url = reverse_lazy('bahan_list')
    
    def form_valid(self, form):
        harga = form.cleaned_data['harga']
        quantity = form.cleaned_data['qty_keseluruhan']
        quantity_terkecil = form.cleaned_data['qty_terkecil']
        
        if quantity != 0:
            harga_kg = harga / quantity
            harga_gram = harga_kg / quantity_terkecil
        else:
            harga_kg = 0
            harga_gram = 0
        
        
        form.instance.harga_kg = harga_kg
        form.instance.harga_gram = harga_gram
        
        return super(BahanCreate, self).form_valid(form)
    
class BahanList(ListView):
    model = MasterBahan
    template_name = 'resep/masterbahan_list.html'
    context_object_name = 'bahans'

class BahanCreate(CreateView):
    model = MasterBahan
    form_class = MasterBahanForm
    success_url = reverse_lazy('bahan_list')
    
    def form_valid(self, form):
        harga = form.cleaned_data['harga']
        quantity = form.cleaned_data['qty_keseluruhan']
        quantity_terkecil = form.cleaned_data['qty_terkecil']
        
        if quantity != 0:
            harga_kg = harga / quantity
        else:
            harga_kg = 0
        
        if quantity_terkecil != 0:
            harga_gram = harga_kg / quantity_terkecil
        else:
            harga_gram = 0
        
        form.instance.harga_kg = harga_kg
        form.instance.harga_gram = harga_gram
        
        return super(BahanCreate, self).form_valid(form)

    
class BahanUpdate(UpdateView):
    model = MasterBahan
    fields = ['kode_bahan', 'nama', 'total', 'qty_keseluruhan', 'qty_terkecil', 'harga', 'harga_jual']
    success_url = reverse_lazy('bahan_list')
    
class BahanDelete(DeleteView):
    model = MasterBahan
    context_object_name = 'bahan'
    success_url = reverse_lazy('bahan_list')

class BahanDetail(DetailView):
    model = MasterBahan
    template_name = 'resep/masterbahan_detail.html'
    context_object_name = 'bahan'
    
class ResepList(ListView):
    model = BarangJadi
    template_name = 'resep/resep_list.html'
    context_object_name = 'barang_jadis'
    
class ResepUpdate(UpdateView):
    model = BarangJadi
    fields = ['nama', 'harga_jual', 'hpp']
    success_url = reverse_lazy('resep_list')

class ResepDelete(DeleteView):
    model = BarangJadi
    context_object_name = 'barang_jadi'
    success_url = reverse_lazy('resep_list')

class ResepDetail(DetailView):
    model = BarangJadi
    template_name = 'resep/resep_detail.html'
    context_object_name = 'barang_jadi'    

# JsonResponse
from django.http import JsonResponse
def cek_bahan(request, id):
    # Mengambil objek bahan dari database berdasarkan id, response dengan jsonj
    bahan = MasterBahan.objects.get(id=id)
    result = {
    "kode_bahan" : bahan.kode_bahan,
    "nama" : bahan.nama,
    "total" : bahan.total,
    "qty_keseluruhan" : bahan.qty_keseluruhan,
    "qty_terkecil" : bahan.qty_terkecil,
    "harga" : bahan.harga,
    "harga_jual" : bahan.harga_jual,
    "harga_kg" : bahan.harga_kg,
    "harga_gram" : bahan.harga_gram,
    "created_date" : bahan.created_date,
    "updated_date" : bahan.updated_date}
    return JsonResponse(result)

def resep_create(request):
    # Mengambil semua bahan yang belum dihapus dari database
    bahans = MasterBahan.objects.filter(is_deleted=False)
    
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

            # Membuat daftar bahan yang akan disimpan dalam bentuk JSON
            daftar_bahan = []
            for i in range(len(id_bahan_list)):
                # Mengambil objek bahan dari database berdasarkan id
                bahan_id = id_bahan_list[i]
                bahan_obj = MasterBahan.objects.get(id=bahan_id)
                print('bahan_obj: ', bahan_obj)
                
                # Membuat dictionary untuk setiap bahan
                bahan = {
                    'id_bahan': bahan_id,
                    'nama_bahan': bahan_obj.nama,
                    'kode_bahan': bahan_obj.kode_bahan,
                    'harga_jual': bahan_obj.harga_jual,
                    'jumlah_satuan': jumlah_satuan_list[i],
                }
                daftar_bahan.append(bahan)

            # Mengubah daftar bahan menjadi format JSON
            daftar_bahan_json = json.dumps(daftar_bahan)

            # Simpan data resep ke dalam database
            barang_jadi = BarangJadi.objects.create(
                nama=nama_roti,
                kode_barang=kode_barang,
                harga_jual=harga_jual,
                daftar_bahan=daftar_bahan_json,
                hpp=hpp,
            )
            

            # Assuming barang_jadi.daftar_bahan is a string representing JSON
            daftar_bahan_dict = json.loads(barang_jadi.daftar_bahan)
            print('daftar_bahan_dict: ', daftar_bahan_dict)
            # get_bahan = daftar_bahan_dict[0]  # Mengakses elemen pertama dalam list
            # nama_bahan = get_bahan['nama_bahan']
            # print('Nama bahan pada elemen pertama:', )  # Output: tepung
            # print('Nama bahan pada elemen pertama:', nama_bahan['jumlah_satuan'])  # Output: tepung
            

      
            # Redirect ke halaman daftar bahan
            return redirect('resep_detail', pk=barang_jadi.id)

    # Mengirimkan data bahan dan form ke template
    context = {'bahans': bahans, 'form': form}
    return render(request, 'resep/resep_form.html', context)
