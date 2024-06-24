
import json

from django.views import View  
from ..models import ResepBahanJadi, MasterBahan, BarangJadi,BahanOlahan
from ..forms import BarangJadiForm, MasterBahanForm, ResepForm, BahanOlahanForm

from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

#Bahan
class BahanOlahCreate(LoginRequiredMixin, CreateView):
    model = BahanOlahan
    form_class = BahanOlahanForm
    template_name = 'bahanOlah/bahanOlah_form.html'
    success_url = reverse_lazy('bahan_olah_list')
    login_url = 'login'
    
    def form_valid(self, form):    
        harga = form.cleaned_data['harga_gram']    
        harga_kg = 0
        nama = form.cleaned_data['nama']
        
        form.instance.nama = nama
        form.instance.harga_kg = harga_kg
        form.instance.harga_gram = harga
        
        print("form.instance",form.instance)
        return super(BahanOlahCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bahans'] = MasterBahan.objects.all()
        url_get_bahan = reverse('cek_bahan', kwargs={'id': 99999})
        context['url_get_bahan'] = url_get_bahan
        print("url_get_bahan",url_get_bahan)
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
    fields = ['kode_bahan', 'nama', 'total', 'qty_keseluruhan', 'qty_terkecil', 'harga', 'harga_jual']
    success_url = reverse_lazy('bahan_olah_list')
    login_url = 'login'
    

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
    