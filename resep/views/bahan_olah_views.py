
import json

from ..models import MasterBahan, BahanOlahan, ResepBahanOlahan, BarangJadi
from ..forms import BahanOlahanForm
from .utils_views import add_resep_to_olah

from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

#Bahan
class BahanOlahCreate(LoginRequiredMixin, CreateView):
    model = BahanOlahan
    form_class = BahanOlahanForm
    template_name = 'bahanOlah/bahanOlah_form.html'
    success_url = reverse_lazy('bahan_olah_list')
    login_url = 'login'
    
    def form_valid(self, form):
        form.instance.save()
        list_bahans = self.request.POST.get('list_bahans')
        list_bahans = json.loads(list_bahans)
        
        add_resep_to_olah(form.instance, list_bahans)

        harga = form.cleaned_data['harga_gram']    
        harga_kg = 0
        nama = form.cleaned_data['nama']
        
        form.instance.nama = nama
        form.instance.harga_kg = harga_kg
        form.instance.harga_gram = harga

        return super(BahanOlahCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bahans'] = MasterBahan.objects.all()
        url_get_bahan = reverse('cek_bahan', kwargs={'id': 99999})
        context['url_get_bahan'] = url_get_bahan
        context['bahan_used'] = []
        return context

class BahanOlahList(LoginRequiredMixin, ListView):
    model = BahanOlahan
    template_name = 'bahanOlah/bahanOlah_list.html'
    context_object_name = 'bahans'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BahanOlahUpdate(LoginRequiredMixin, UpdateView):
    model = BahanOlahan
    template_name = 'bahanOlah/bahanOlah_form.html'
    form_class = BahanOlahanForm
    success_url = reverse_lazy('bahan_olah_list')
    login_url = 'login'

    def get_context_data(self, **kwargs):
        print("BAHAN OLAH UPDATE")
        context = super().get_context_data(**kwargs)
        context['bahans'] = MasterBahan.objects.all()
        url_get_bahan = reverse('cek_bahan', kwargs={'id': 99999})
        context['url_get_bahan'] = url_get_bahan
        bahan_used = ResepBahanOlahan.objects.filter(bahan_olahan=self.object)
        bahan_used_list = []
        for item in bahan_used:
            bahan_used_list.append({
                'id': item.id,
                'master_bahan_id': item.master_bahan_id,
                'bahan_olahan_id': item.bahan_olahan_id,
                'jumlah_pemakaian': item.jumlah_pemakaian,
                'is_deleted': str(item.is_deleted).lower()  # Convert boolean to lowercase string
            })
        
        context['bahan_used'] = bahan_used_list
        
        print("url_get_bahan",url_get_bahan)
        return context
    
    def form_valid(self, form):
        ResepBahanOlahan.objects.filter(bahan_olahan=self.object).delete()
        # list_bahans
        list_bahans = self.request.POST.get('list_bahans')
        list_bahans = json.loads(list_bahans)
        
        add_resep_to_olah(self.object, list_bahans)
        return super(BahanOlahUpdate, self).form_valid(form)
    

class BahanOlahDelete(LoginRequiredMixin, DeleteView):
    model = BahanOlahan
    context_object_name = 'bahan'
    template_name = 'bahanOlah/bahanOlah_confirm_delete.html'
    success_url = reverse_lazy('bahan_olah_list')
    login_url = 'login'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.used_in_recipe:
            return HttpResponseRedirect(reverse('error_page'))  
        
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

class BahanOlahDetail(LoginRequiredMixin, DetailView):
    model = BahanOlahan
    template_name = 'bahanOlah/bahanOlah_detail.html'
    context_object_name = 'bahan_olah_list'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bahan_olah = BahanOlahan.objects.get(id=self.kwargs['pk'])
        context['bahan_olah'] = bahan_olah
        # bahans
        bahans = []
        for rbo in ResepBahanOlahan.objects.filter(bahan_olahan=bahan_olah):
            bahan = MasterBahan.objects.get(id=rbo.master_bahan_id)
            result = {}
            result['nama'] = bahan.nama
            result['kode_bahan'] = bahan.kode_bahan
            result['jumlah'] = rbo.jumlah_pemakaian
            result['harga_gram'] = bahan.harga_gram
            result['total_hpp_single_bahan'] = bahan.harga_gram * rbo.jumlah_pemakaian
            bahans.append(result)
        context['bahans'] = bahans
        return context


@login_required(login_url='login')
# Fungsi untuk mengecek detail bahan dan merespons dalam format JSON
def cek_bahan_olah(request, id):
    # Mengambil objek bahan dari database berdasarkan id
    bahan = BahanOlahan.objects.get(id=id)
    # Menyiapkan data bahan dalam format JSON
    result = {
        "kode_bahan": "olahan_"+str(bahan.id),
        "nama": bahan.nama,
        "total": bahan.total,
        "qty_keseluruhan": bahan.qty_keseluruhan,
        "qty_terkecil": bahan.qty_terkecil,
        "harga": bahan.harga,
        "harga_kg": bahan.harga_kg,
        "harga_gram": bahan.harga_gram,
        "created_date": bahan.created_date,
        "updated_date": bahan.updated_date
    }
    # Mengirimkan response dalam format JSON
    return JsonResponse(result)

@login_required(login_url='login')
# Fungsi untuk mengecek detail bahan dan merespons dalam format JSON
def cek_resep(request, id):
    # Mengambil objek bahan dari database berdasarkan id
    barang_jadi = BarangJadi.objects.get(id=id)
    # Menyiapkan data bahan dalam format JSON
    result = {
        "kode_barang": "barang_"+str(barang_jadi.id),
        "nama": barang_jadi.nama,
        "harga_jual": barang_jadi.harga_jual,
        "hpp": barang_jadi.hpp,
    }
    # Mengirimkan response dalam format JSON
    return JsonResponse(result)