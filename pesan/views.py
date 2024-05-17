from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy

from resep.forms import ResepForm
from resep.models import BarangJadi, MasterBahan, Resep
from .models import Pesanan, ListPesanan
from .forms import PesananForm, ListPesananForm

def cek_pesanan(request, id):
    resep = Resep.objects.get(id=id)
    result = {
        "kode_bahan": resep.master_bahan.nama,
        "nama": resep.barang_jadi.nama,
        "total": resep.jumlah_pemakaian,
    }
    # Mengirimkan response dalam format JSON
    return JsonResponse(result)

def PesananCreate(request):
    daftar_resep = Resep.objects.filter(is_deleted=False)
    
    form = ResepForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            nama = request.POST.get('nama')
            print('nama: ', nama)
            # alamat = request.POST.get('alamat')
            # pesanan = request.POST.get('pesanan')
            # tanggal_pesan = request.POST.get('tanggal_pesan')
            # total_harga = request.POST.get('total_harga')
            # total_bayar = request.POST.get('total_bayar')
            # harga_modal = request.POST.get('harga_modal')
            # nomor_telp = request.POST.get('nomor_telp')
            # catatan = request.POST.get('catatan')
            
            id_resep_list = request.POST.getlist('all_resep[]')
            print('id_resep_list: ', id_resep_list)
            jumlah_satuan_list = request.POST.getlist('jumlah_satuan[]')
            print('jumlah_satuan_list: ', jumlah_satuan_list)
            
       
            # return redirect('pesanan_list', pk=barang_jadi.id)

    return render(request, 'pesanan_create.html', locals())

class PesananListView(ListView):
    model = Pesanan
    template_name = 'pesanan_list.html'
    context_object_name = 'pesanan_list'
    
class PesananDetailView(DetailView):
    model = Pesanan
    template_name = 'pesanan_detail.html'

class PesananUpdateView(UpdateView):
    model = Pesanan
    form_class = PesananForm
    template_name = 'pesanan_update.html'
    success_url = reverse_lazy('pesanan_list')

class PesananDeleteView(DeleteView):
    model = Pesanan
    success_url = reverse_lazy('pesanan_list')
