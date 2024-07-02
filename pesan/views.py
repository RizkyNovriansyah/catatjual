from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from resep.forms import ResepForm
from resep.models import BarangJadi, MasterBahan, ResepBahanJadi
from .models import Pesanan, ListPesanan
from .forms import PesananForm, ListPesananForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

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

# @login_required(login_url='login')
# def PesananCreate(request):
#     daftar_resep = ResepBahanJadi.objects.filter(is_deleted=False)

#     if request.method == 'POST':
#         nama = request.POST.get('nama_pembeli')
#         alamat = request.POST.get('alamat_pembeli')
#         tanggal_pesan = request.POST.get('tanggal_pesan')
#         total_bayar = int(request.POST.get('total_bayar', 0))
#         nomor_telp = request.POST.get('nomor_telp_pembeli')
#         catatan = request.POST.get('catatan_pembeli')

#         id_roti_list = request.POST.getlist('roti_list[]')
#         jumlah_list = request.POST.getlist('jumlah_list[]')

#         # Initialize total_harga and harga_modal
#         total_harga = 0
#         harga_modal = 0
        
#         # Calculate total_harga and harga_modal
#         for i, roti_id in enumerate(id_roti_list):
#             barang_jadi = BarangJadi.objects.get(id=roti_id)
#             jumlah = int(jumlah_list[i])
#             harga = barang_jadi.harga_jual
#             modal = barang_jadi.hpp
#             total_harga += harga * jumlah
#             harga_modal += modal * jumlah
        
#         pesanan_list = {}    
#         for roti_id in id_roti_list:
#             barang_jadi = BarangJadi.objects.get(id=roti_id)
#             pesanan_list[roti_id] = {
#                 'nama' : barang_jadi.nama,
#                 'kode_barang' : barang_jadi.kode_barang,
#                 'harga_jual' : barang_jadi.harga_jual,
#                 'daftar_bahan' : barang_jadi.daftar_bahan,
#                 'hpp' : barang_jadi.hpp,
#             }
            
#         pesanan = Pesanan.objects.create(
#             nama=nama,
#             alamat=alamat,
#             pesanan=pesanan_list,
#             tanggal_pesan=tanggal_pesan,
#             total_harga=total_harga,
#             total_bayar=total_bayar,
#             harga_modal=harga_modal,
#             nomor_telp=nomor_telp,
#             catatan=catatan
#         )

#         # Create ListPesanan entries
#         for i, roti_id in enumerate(id_roti_list):
#             barang_jadi = BarangJadi.objects.get(id=roti_id)
#             jumlah = int(jumlah_list[i])
#             ListPesanan.objects.create(
#                 pesanan=pesanan,
#                 barang_jadi=barang_jadi,
#                 jumlah_barang_jadi=jumlah
#             )

#         return redirect('pesanan_list')

#     return render(request, 'pesanan_create.html', {'daftar_resep': daftar_resep})

class PesananCreate(CreateView):
    model = Pesanan
    form_class = PesananForm
    template_name = 'pesanan_create.html'
    success_url = reverse_lazy('pesanan_list')
    login_url = 'login'

    def form_valid(self, form):
        # Additional processing if needed before saving the form
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Additional context data if needed
        daftar_resep = ResepBahanJadi.objects.filter(is_deleted=False)
        context['daftar_resep'] = daftar_resep
        context['url_get_roti'] = reverse('cek_resep', kwargs={'id': 99999})
        print(context['url_get_roti'])
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
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Additional context data if needed
        daftar_resep = ResepBahanJadi.objects.filter(is_deleted=False)
        context['daftar_resep'] = daftar_resep
        context['url_get_roti'] = reverse('cek_resep', kwargs={'id': 99999})
        print(context['url_get_roti'])
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

