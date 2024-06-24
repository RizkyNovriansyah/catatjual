
import json

from django.views import View  
from ..models import ResepBahanJadi, MasterBahan, BarangJadi
from ..forms import BarangJadiForm, MasterBahanForm, ResepForm

from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

#Bahan
class BahanOlahCreate(LoginRequiredMixin, CreateView):
    model = MasterBahan
    form_class = MasterBahanForm
    template_name = 'bahanOlah/bahanOlah_form.html'
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
        
        return super(BahanOlahCreate, self).form_valid(form)
    

class BahanOlahList(LoginRequiredMixin, ListView):
    model = MasterBahan
    template_name = 'bahanOlah/bahanOlah_list.html'
    context_object_name = 'bahans'
    login_url = 'login'


class BahanOlahUpdate(LoginRequiredMixin, UpdateView):
    model = MasterBahan
    template_name = 'bahanOlah/bahanOlah_form.html'
    fields = ['kode_bahan', 'nama', 'total', 'qty_keseluruhan', 'qty_terkecil', 'harga', 'harga_jual']
    success_url = reverse_lazy('bahan_list')
    login_url = 'login'
    

class BahanOlahDelete(LoginRequiredMixin, DeleteView):
    model = MasterBahan
    context_object_name = 'bahan'
    template_name = 'bahanOlah/bahanOlah_confirm_delete.html'
    success_url = reverse_lazy('bahan_list')
    login_url = 'login'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.used_in_recipe:
            return HttpResponseRedirect(reverse('error_page'))  
        
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

class BahanOlahDetail(LoginRequiredMixin, DetailView):
    model = MasterBahan
    template_name = 'bahanOlah/bahanOlah_detail.html'
    context_object_name = 'bahan'
    login_url = 'login'
    