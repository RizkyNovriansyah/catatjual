
import json

from django.views import View  
from ..models import MasterBahan, ResepBahanJadi, ResepBahanOlahan, ResepOlahanJadi
from ..forms import BarangJadiForm, MasterBahanForm, ResepForm

from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

#Bahan
class BahanCreate(LoginRequiredMixin, CreateView):
    model = MasterBahan
    form_class = MasterBahanForm
    template_name = 'bahan/masterbahan_form.html'
    success_url = reverse_lazy('bahan_list')
    login_url = 'login'
    
    def form_valid(self, form):    
        harga = form.cleaned_data['harga']    
        quantity = form.cleaned_data['qty_keseluruhan']    
        quantity_terkecil = 1

        if quantity != 0:
            harga_kg = harga / quantity
            harga_gram = harga_kg / quantity_terkecil
        else:
            harga_kg = 0
            harga_gram = 0
        
        form.instance.harga_kg = harga_kg
        form.instance.harga_gram = harga_gram
        
        return super(BahanCreate, self).form_valid(form)
    

class BahanList(LoginRequiredMixin, ListView):
    model = MasterBahan
    template_name = 'bahan/masterbahan_list.html'
    context_object_name = 'bahans'
    login_url = 'login'


class BahanUpdate(LoginRequiredMixin, UpdateView):
    model = MasterBahan
    template_name = 'bahan/masterbahan_form.html'
    # fields = ['kode_bahan', 'nama', 'total', 'qty_keseluruhan', 'qty_terkecil', 'harga', 'harga_jual']
    success_url = reverse_lazy('bahan_list')
    login_url = 'login'
    form_class = MasterBahanForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # get id 
        id = self.kwargs.get('pk')
        # get object
        bahan = MasterBahan.objects.get(id=id) 
        # Optionally, set initial data for the form fields
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bahan = MasterBahan.objects.get(id=self.kwargs.get('pk'))
        context['bahan'] = bahan

        # potensi kenaikan harga olahan
        list_bahan_olahan = []
        for resep_bahan_olahan in ResepBahanOlahan.objects.filter(master_bahan=self.object):
            bahan_olahan = resep_bahan_olahan.bahan_olahan
            bo = {
                "bahan_olahan__id": bahan_olahan.id,
                "bahan_olahan__nama": bahan_olahan.nama,
                "bahan_olahan__hpp": bahan_olahan.harga_gram,
                "jumlah_pemakaian": resep_bahan_olahan.jumlah_pemakaian,
                "resep_olahan_jadi": []
            }

            print("resep_bahan_olahan.harga_gram",resep_bahan_olahan.jumlah_pemakaian)

            for resep_olahan_jadi in ResepOlahanJadi.objects.filter(bahan_olahan=bahan_olahan):
                barang_jadi = resep_olahan_jadi.barang_jadi
                roj = {
                    "id": resep_olahan_jadi.id,
                    "barang_jadi__id": resep_olahan_jadi.barang_jadi.id,
                    "barang_jadi__nama": barang_jadi.nama,
                    "barang_jadi__hpp": barang_jadi.hpp,
                    "barang_jadi__harga_jual": barang_jadi.harga_jual,
                    "jumlah_pemakaian": resep_olahan_jadi.jumlah_pemakaian,   
                }
                bo['resep_olahan_jadi'].append(roj)

            list_bahan_olahan.append(bo)
        
        context['list_bahan_olahan'] = list_bahan_olahan
        # print(context['list_bahan_olahan'])

        # potensi kenaikan harga roti
        list_barang_jadi = []
        for resep_bahan_jadi in ResepBahanJadi.objects.filter(master_bahan=self.object):
            barang_jadi = resep_bahan_jadi.barang_jadi
            bj = {
                "barang_jadi__id": barang_jadi.id,
                "barang_jadi__nama": barang_jadi.nama,
                "barang_jadi__hpp": barang_jadi.hpp,
                "barang_jadi__harga_jual": barang_jadi.harga_jual,
                "jumlah_pemakaian": resep_bahan_jadi.jumlah_pemakaian,
            }

            list_barang_jadi.append(bj)
        context['list_barang_jadi'] = list_barang_jadi
        return context
    
    def form_valid(self, form):

        harga = form.cleaned_data['harga']    
        quantity = form.cleaned_data['qty_keseluruhan']    
        quantity_terkecil = quantity
        harga_gram = float(harga / quantity_terkecil)
        print(harga,quantity,harga_gram)

        form.instance.harga_gram = harga_gram
        
        return super(BahanUpdate, self).form_valid(form)

class BahanDelete(LoginRequiredMixin, DeleteView):
    model = MasterBahan
    context_object_name = 'bahan'
    template_name = 'bahan/masterbahan_confirm_delete.html'
    success_url = reverse_lazy('bahan_list')
    login_url = 'login'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.used_in_recipe:
            return HttpResponseRedirect(reverse('error_page'))  
        
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

class BahanDetail(LoginRequiredMixin, DetailView):
    model = MasterBahan
    template_name = 'bahan/masterbahan_detail.html'
    context_object_name = 'bahan'
    login_url = 'login'


@login_required(login_url='login')
# Fungsi untuk mengecek detail bahan dan merespons dalam format JSON
def cek_bahan(request, id):
    # Mengambil objek bahan dari database berdasarkan id
    bahan = MasterBahan.objects.get(id=id)
    print('bahan: ', bahan)
    print("nama bahan",bahan.nama)
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
