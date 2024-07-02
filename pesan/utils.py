# views.py
from .models import ListPesanan
# from BarangJadi
from resep.models import BarangJadi
from django.views.generic.base import TemplateView

class ErrorPageView(TemplateView):
    template_name = 'error_page.html'  # Ganti 'error_page.html' dengan nama template halaman error Anda

def add_pesanan(pesanan,list_rotis):
    ListPesanan.objects.filter(pesanan=pesanan).delete()
    for data_roti in list_rotis:
        id = data_roti['id'].split('-')[1].split('_')[1]
        roti = BarangJadi.objects.get(id=id)
        jumlah = data_roti['value']
        lp = ListPesanan.objects.create(
            pesanan = pesanan,
            barang_jadi = roti,
            jumlah_barang_jadi = jumlah
        )
        # pesanan = models.ForeignKey(Pesanan, on_delete=models.CASCADE, related_name='list_pesanan')
        # barang_jadi = models.ForeignKey(BarangJadi, on_delete=models.CASCADE)
        # jumlah_barang_jadi = models.IntegerField(default=0)
        