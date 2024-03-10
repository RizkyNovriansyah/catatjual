# views.py
from .models import Resep, MasterBahan, BarangJadi
from .forms import MasterBahanForm, SelectBahanForm, ResepForm
from django.db.models import Sum

from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy


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
    
# class ResepList(ListView):
#     model = BarangJadi
#     template_name = 'resep/resep_list.html'
#     context_object_name = 'barang_jadis'
    
def resep_list(request):
    barang_jadi = BarangJadi.objects.all()
    return render(request, 'resep/resep_list.html', locals())
    
class ResepUpdate(UpdateView):
    model = BarangJadi
    fields = ['nama', 'harga_jual', 'hpp']
    success_url = reverse_lazy('resep_list')

class ResepDelete(DeleteView):
    model = BarangJadi
    context_object_name = 'barang_jadi'
    success_url = reverse_lazy('resep_list')

# Di dalam views.py

def resep_create(request):
    bahans = MasterBahan.objects.filter(is_deleted=False)

    if request.method == 'POST':
        nama = request.POST.get('nama')
        kode_barang = request.POST.get('kode_barang')
        harga_jual = request.POST.get('harga_jual')
        bahan_digunakan = request.POST.getlist('bahans') # yang kepake
        bahans_id = request.POST.getlist('bahans_id')
        bahans_jumlah = request.POST.getlist('bahans_jumlah_')
        
        barang_jadi = BarangJadi.objects.create(
            nama=nama,
            harga_jual=harga_jual,
            kode_barang=kode_barang,
            daftar_bahan=bahan_digunakan
        )
        
        total_hpp = 0
        for bahan_id in bahan_digunakan:
            bahan_jumlah_key = 'bahans_jumlah_' + bahan_id
            bahan_jumlah = request.POST.get(bahan_jumlah_key)
            if bahan_jumlah:
                bahan = MasterBahan.objects.get(id=bahan_id)
                print('bahan: ', bahan)
                harga_per_bahan = bahan.qty_terkecil
                print('harga_per_bahan: ', harga_per_bahan)
                total_hpp += int(harga_per_bahan) * int(bahan_jumlah)
                print('total_hpp: ', total_hpp)
                Resep.objects.create(
                    master_bahan=bahan,
                    barang_jadi=barang_jadi,
                    jumlah_pemakaian=bahan_jumlah
                )

        barang_jadi.hpp = total_hpp
        barang_jadi.save()
        return redirect('resep_list')

    context = {'bahans': bahans}
    return render(request, 'resep/resep_form.html', context)


class ResepDetail(DetailView):
    model = BarangJadi
    template_name = 'resep/resep_detail.html'
    context_object_name = 'barang_jadi' 

def index(request):
    context = {'form': SelectBahanForm(), 'data': MasterBahan.objects.all()}
    return render(request, 'resep/index.html', context)

def index_create(request):
    context = {'form': SelectBahanForm()}
    if request.method == 'POST':
        form = SelectBahanForm(request.POST or None)
        if form.is_valid():
            index = form.save()
            context = {'index': index}
            return render(request, 'includes/view_index.html', context)
    return render(request, 'includes/form.html', context)
