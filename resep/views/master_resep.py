import json

from django.views import View  
from ..models import ResepBahanJadi, MasterBahan, BarangJadi
from ..forms import BarangJadiForm, MasterBahanForm, ResepForm
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

class MasterResepList(LoginRequiredMixin, ListView):
    model = BarangJadi
    template_name = 'resep/resep_list.html'
    context_object_name = 'barang_jadis'
    login_url = 'login'
    
    def get_queryset(self):
        return BarangJadi.objects.filter(is_deleted=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class MasterResepDelete(DeleteView):
    model = BarangJadi
    context_object_name = 'barang_jadi'
    success_url = reverse_lazy('master_resep_list')

class MasterResepDetail(DetailView):
    model = BarangJadi
    template_name = 'masterResep/master_resep_detail.html'
    context_object_name = 'barang_jadi'   
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selisih = self.object.harga_jual - self.object.hpp
        id_bahan = self.object.id
        resep = ResepBahanJadi.objects.filter(barang_jadi__id=id_bahan)
        
        bahans = []
        for bahan in resep:
            nama = bahan.master_bahan.nama
            jumlah = bahan.jumlah_pemakaian
            total_hpp_single_bahan = bahan.master_bahan.harga_gram * jumlah
            bahans.append({'nama' : nama, 
                           'jumlah' : jumlah,
                           'kode_bahan' : bahan.master_bahan.kode_bahan,
                           'harga_gram': bahan.master_bahan.harga_gram,
                           'total_hpp_single_bahan' : total_hpp_single_bahan,
                           })
            
        context['bahans'] = bahans
        context['selisih'] = selisih
        return context
def cek_bahan(request, id):
    bahan = MasterBahan.objects.get(id=id)
    print('bahan: ', bahan)
    print("nama bahan",bahan.nama)
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
    return JsonResponse(result)
def master_resep_create(request):
    bahans = MasterBahan.objects.filter(is_deleted=False)
    form = ResepForm(request.POST or None)

    if request.method == 'POST':
        
        if form.is_valid():
            
            nama_roti = request.POST.get('nama_roti')
            kode_barang = request.POST.get('kode_barang')
            harga_jual = request.POST.get('harga_jual')
            hpp = request.POST.get('hpp')
            
            id_bahan_list = request.POST.getlist('id_bahan[]')
            jumlah_satuan_list = request.POST.getlist('jumlah_satuan[]')
            master_bahan = True
            print('master_bahan: ', master_bahan)
            barang_jadi = BarangJadi.objects.create(
                nama=nama_roti,
                kode_barang=kode_barang,
                harga_jual=harga_jual,
                hpp=hpp,
                master_roti = master_bahan,
            )
            barang_jadi_check = barang_jadi.master_roti
            print('barang_jadi_check: ', barang_jadi_check)
            
            daftar_bahan = []
            for i in range(len(id_bahan_list)):
                bahan_id = id_bahan_list[i]
                bahan_obj = MasterBahan.objects.get(id=bahan_id)
                
                """ Mekanisme Kotor
                bahan = {
                    'id_bahan': bahan_id,
                    'nama_bahan': bahan_obj.nama,
                    'kode_bahan': bahan_obj.kode_bahan,
                    'harga_jual': harga_jual,
                    'jumlah_satuan': jumlah_satuan_list[i],                    
                }
                daftar_bahan.append(bahan)
                """
                
                resep_create = ResepBahanJadi.objects.create(
                    master_bahan = bahan_obj,
                    barang_jadi  = barang_jadi, 
                    jumlah_pemakaian = jumlah_satuan_list[i],
                )
            
            """ Mekanisme Kotor   
            daftar_bahan_json = json.dumps(daftar_bahan)
            barang_jadi.daftar_bahan = daftar_bahan_json
            barang_jadi.save()
            """
          
            return redirect('resep_detail', pk=barang_jadi.id)

    context = {'bahans': bahans, 'form': form}
    return render(request, 'masterResep/master_resep_form.html', locals())

class MasterResepUpdateView(UpdateView):
    model = BarangJadi
    form_class = BarangJadiForm
    template_name = 'masterResep/master_resep_update.html'
    success_url = '/'
    context_object_name = 'barang_jadi'
    

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
        
        self.object.nama = nama_roti
        self.object.kode_barang = kode_barang
        self.object.harga_jual = harga_jual
        self.object.hpp = hpp
        self.object.save()

        ResepBahanJadi.objects.filter(barang_jadi=self.object).delete()

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
        return reverse_lazy('master_resep_detail', kwargs={'pk': self.object.id})