# views.py
from .models import Resep, MasterBahan, BarangJadi
from .forms import MasterBahanForm, ResepForm
from django.db.models import Sum

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
        else:
            harga_kg = 0
        
        if quantity_terkecil != 0:
            harga_gram = harga_kg / quantity_terkecil
        else:
            harga_gram = 0
        
        form.instance.harga_kg = harga_kg
        form.instance.harga_gram = harga_gram
        
        return super(BahanCreate, self).form_valid(form)
    
class BahanList(ListView):
    model = MasterBahan
    template_name = 'resep/masterbahan_list.html'
    context_object_name = 'bahans'

class BahanDetail(DetailView):
    model = MasterBahan
    template_name = 'resep/masterbahan_detail.html'
    context_object_name = 'bahan'

class BahanUpdate(UpdateView):
    model = MasterBahan
    fields = ['kode_bahan', 'nama', 'total', 'qty_keseluruhan', 'qty_terkecil', 'harga', 'harga_jual']
    success_url = reverse_lazy('bahan_list')
    
class BahanDelete(DeleteView):
    model = MasterBahan
    context_object_name = 'bahan'
    success_url = reverse_lazy('bahan_list')
    


#Resep
class ResepCreate(FormView):
    form_class = ResepForm
    template_name = 'resep/resep_form.html'
    success_url = reverse_lazy('resep_list')
    
    def form_valid(self, form):
        nama = self.request.POST.get('nama')
        kode_barang = self.request.POST.get('kode_barang')
        harga_jual = self.request.POST.get('harga_jual')
        bahan_digunakan = self.request.POST.getlist('bahans')
        
        barang_jadi = BarangJadi.objects.create(
            nama=nama,
            harga_jual=harga_jual,
            kode_barang=kode_barang,
            daftar_bahan=bahan_digunakan
        )
        
        total_hpp = 0
        if bahan_digunakan:
            for bahan_id in bahan_digunakan:
                bahan_jumlah_key = 'bahans_jumlah_' + bahan_id
                bahan_jumlah = form.cleaned_data[bahan_jumlah_key]
                print('bahan_jumlah: ', bahan_jumlah)
                if bahan_jumlah:
                    bahan = MasterBahan.objects.get(id=bahan_id)
                    harga_per_bahan = bahan.qty_terkecil
                    print('harga_per_bahan: ', harga_per_bahan)
                    total_hpp += int(harga_per_bahan) * int(bahan_jumlah)
                    Resep.objects.create(
                        master_bahan=bahan,
                        barang_jadi=barang_jadi,
                        jumlah_pemakaian=bahan_jumlah
                    )

            barang_jadi.hpp = total_hpp
            barang_jadi.save()
        return super(ResepCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(ResepCreate, self).get_context_data(**kwargs)
        context['bahans'] = MasterBahan.objects.filter(is_deleted=False)
        return context
       
class ResepList(ListView):
    model = BarangJadi
    template_name = 'resep/resep_list.html'
    context_object_name = 'barang_jadis'
 
class ResepDetail(DetailView):
    model = BarangJadi
    template_name = 'resep/resep_detail.html'
    context_object_name = 'barang_jadi'    

class ResepUpdate(UpdateView):
    model = BarangJadi
    fields = ['nama', 'harga_jual', 'hpp']
    success_url = reverse_lazy('resep_list')

class ResepDelete(DeleteView):
    model = BarangJadi
    context_object_name = 'barang_jadi'
    success_url = reverse_lazy('resep_list')
