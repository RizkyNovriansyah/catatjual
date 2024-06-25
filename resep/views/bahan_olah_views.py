
import json

from django.views import View  
from ..models import ResepBahanJadi, MasterBahan, BarangJadi,BahanOlahan,ResepOlahanJadi, ResepBahanOlahan
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
        list_bahans = self.request.POST.getlist('list_bahans')

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
    form_class = BahanOlahanForm
    success_url = reverse_lazy('bahan_olah_list')
    login_url = 'login'

    def get_context_data(self, **kwargs):
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
        # list_bahans
        list_bahans = self.request.POST.get('list_bahans')
        list_bahans = json.loads(list_bahans)
        print("list_bahans",list_bahans)
        for bahan in list_bahans:
            kode_bahan = bahan['id'].split("#")[1]
            mb = MasterBahan.objects.get(kode_bahan=kode_bahan)
            rbo = ResepBahanOlahan.objects.create(
                bahan_olahan = self.object,
                master_bahan = mb,
                jumlah_pemakaian = bahan['value']
            )
            rbo.save()
            print("rbo",rbo, rbo.bahan_olahan,rbo.master_bahan,rbo.jumlah_pemakaian)

        harga = form.cleaned_data['harga_gram']    
        harga_kg = 0
        nama = form.cleaned_data['nama']
        
        form.instance.nama = nama
        form.instance.harga_kg = harga_kg
        form.instance.harga_gram = harga
        
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
    