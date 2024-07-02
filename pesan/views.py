from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from resep.forms import ResepForm
from resep.models import BarangJadi, MasterBahan, ResepBahanJadi
from .models import Pesanan, ListPesanan
from .forms import PesananForm, ListPesananForm
from .utils import add_pesanan
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
import json
from django.utils import formats

@login_required(login_url='login')
def cek_pesanan(request, id):
    resep = ResepBahanJadi.objects.get(id=id)
    result = {
        "kode_resep": resep.barang_jadi.kode_barang,
        "nama": resep.barang_jadi.nama,
        "harga_jual": resep.barang_jadi.harga_jual,
        "hpp": resep.barang_jadi.hpp,
    }
    # Mengirimkan response dalam format JSON
    return JsonResponse(result)

class PesananCreate(CreateView):
    model = Pesanan
    form_class = PesananForm
    template_name = 'pesanan_create.html'
    success_url = reverse_lazy('pesanan_list')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.save()
        
        list_bahans = self.request.POST.get('list_bahans')
        list_bahans = json.loads(list_bahans)
        add_pesanan(form.instance, list_bahans)

        # tanggal_pesan
        tanggal_pesan = form.cleaned_data.get('tanggal_pesan')
        print(tanggal_pesan)
        instance = form.instance
        instance.tanggal_pesan = tanggal_pesan
        instance.save()

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Additional context data if needed
        daftar_resep = ResepBahanJadi.objects.filter(is_deleted=False)
        context['daftar_resep'] = daftar_resep
        context['url_get_roti'] = reverse('cek_resep', kwargs={'id': 99999})
        context['pesanan_used'] = []
        return context
    
class PesananListView(LoginRequiredMixin, ListView):
    model = Pesanan
    template_name = 'pesanan_list.html'
    login_url = 'login'
    def get_context_data(self, **kwargs):
        pesanan_list = Pesanan.objects.filter(is_deleted=False)
        context = {
            'pesanan_list': pesanan_list,
        }
        return context
    

class PesananDetailView(LoginRequiredMixin, DetailView):
    model = Pesanan
    template_name = 'pesanan_detail.html'
    login_url = 'login'

class PesananUpdate(UpdateView):
    model = Pesanan
    form_class = PesananForm
    template_name = 'pesanan_create.html'
    success_url = reverse_lazy('pesanan_list')
    login_url = 'login'  # Optional: Specify login URL if login required for this view

    def form_valid(self, form):
        # Additional processing before saving the form
        # Example: Modify form data or perform additional validations

        # get list_bahans
        list_bahans = self.request.POST.get('list_bahans')
        list_bahans = json.loads(list_bahans)
        
        add_pesanan(form.instance, list_bahans)

        # tanggal_pesan
        tanggal_pesan = form.cleaned_data.get('tanggal_pesan')
        print(tanggal_pesan)
        instance = form.instance
        instance.tanggal_pesan = tanggal_pesan
        instance.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Additional context data if needed
        daftar_resep = ResepBahanJadi.objects.filter(is_deleted=False)
        context['daftar_resep'] = daftar_resep
        context['url_get_roti'] = reverse('cek_resep', kwargs={'id': 99999})
        pesanan_used = ListPesanan.objects.filter(pesanan=self.object)

        pesanan_used_list = []
        for item in pesanan_used:
            print(item,item.jumlah_barang_jadi)
            pesanan_used_list.append({
                'id': item.id,
                'barang_jadi': item.barang_jadi.id,
                'jumlah_pemakaian': item.jumlah_barang_jadi,
                'is_deleted': str(item.is_deleted).lower()  # Convert boolean to lowercase string
            })
        
        context['pesanan_used'] = pesanan_used_list
        print(context['url_get_roti'])
        # tanggal_pesan
        print(self.object.tanggal_pesan)
        try:
            context['tanggal_pesan'] = self.object.tanggal_pesan.strftime('%Y-%m-%d')
        except:
            context['tanggal_pesan'] = None

        return context

@login_required(login_url='login')
def PesananDelete(request, pk):
    pesanan = get_object_or_404(Pesanan, pk=pk)
    pesanan.is_deleted = True
    pesanan.save()
    list_pesanan = ListPesanan.objects.filter(pesanan=pesanan)
    for item in list_pesanan:
        item.is_deleted = True
        item.save()
        
    return redirect('pesanan_list')

