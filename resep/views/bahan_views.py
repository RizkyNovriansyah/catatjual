
import json

from django.views import View  
from ..models import Resep, MasterBahan, BarangJadi
from ..forms import BarangJadiForm, MasterBahanForm, ResepForm

from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView


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
    template_name = 'bahan/masterbahan_list.html'
    context_object_name = 'bahans'


class BahanUpdate(UpdateView):
    model = MasterBahan
    template_name = 'bahan/masterbahan_form.html'
    fields = ['kode_bahan', 'nama', 'total', 'qty_keseluruhan', 'qty_terkecil', 'harga', 'harga_jual']
    success_url = reverse_lazy('bahan_list')
    

class BahanDelete(DeleteView):
    model = MasterBahan
    context_object_name = 'bahan'
    template_name = 'bahan/masterbahan_confirm_delete.html'
    success_url = reverse_lazy('bahan_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.used_in_recipe:
            return HttpResponseRedirect(reverse('error_page'))  
        
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

class BahanDetail(DetailView):
    model = MasterBahan
    template_name = 'bahan/masterbahan_detail.html'
    context_object_name = 'bahan'
    