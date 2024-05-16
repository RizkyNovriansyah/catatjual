from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy

from resep.forms import ResepForm
from resep.models import BarangJadi, MasterBahan, Resep
from .models import Pesanan, ListPesanan
from .forms import PesananForm, ListPesananForm

def PesananCreate(request):
    bahans = MasterBahan.objects.filter(is_deleted=False)
    masters = BarangJadi.objects.filter(master_roti=True)
    
    form = ResepForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            nama_roti = request.POST.get('nama_roti')
            kode_barang = request.POST.get('kode_barang')
            harga_jual = request.POST.get('harga_jual')
            hpp = request.POST.get('hpp')
            
            id_bahan_list = request.POST.getlist('id_bahan[]')
            jumlah_satuan_list = request.POST.getlist('jumlah_satuan[]')
            
            barang_jadi = BarangJadi.objects.create(
                nama=nama_roti,
                kode_barang=kode_barang,
                harga_jual=harga_jual,
                hpp=hpp,
            )
            
            daftar_bahan = []
            for i in range(len(id_bahan_list)):
                bahan_id = id_bahan_list[i]
                bahan_obj = MasterBahan.objects.get(id=bahan_id)
           
                resep_create = Resep.objects.create(
                    master_bahan = bahan_obj,
                    barang_jadi  = barang_jadi, 
                    jumlah_pemakaian = jumlah_satuan_list[i],
                )
       
            return redirect('pesanan_list', pk=barang_jadi.id)

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
