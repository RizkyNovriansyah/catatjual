from django import forms
from .models import Pesanan, ListPesanan

class PesananForm(forms.ModelForm):
    class Meta:
        model = Pesanan
        fields = ['nama', 'pesanan']

class ListPesananForm(forms.ModelForm):
    class Meta:
        model = ListPesanan
        fields = ['pesanan', 'barang_jadi', 'jumlah_barang_jadi']
