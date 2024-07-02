from django import forms
from .models import Pesanan, ListPesanan

class PesananForm(forms.ModelForm):
    class Meta:
        model = Pesanan
        fields = ['nama', 'alamat', 'tanggal_pesan', 'total_harga', 'total_bayar', 'harga_modal', 'nomor_telp', 'catatan']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Update widget attributes for each field
        self.fields['nama'].widget.attrs.update({'class': 'form-control','placeholder': 'Nama Pembeli'})
        self.fields['alamat'].widget.attrs.update({'class': 'form-control','placeholder': 'Alamat Pembeli'})
        # self.fields['tanggal_pesan'].widget.attrs.update({'class': 'form-control', 'type': 'date', 'placeholder': 'Masukan Tanggal'})
        
        self.fields['total_harga'].widget.attrs.update({'class': 'form-control','placeholder': 'Total Harga', 'id':'total_harga_input'})
        self.fields['total_bayar'].widget.attrs.update({'class': 'form-control','placeholder': 'Total Bayar'}) 
        self.fields['harga_modal'].widget.attrs.update({'class': 'form-control','placeholder': 'Harga Modal'}) 
        self.fields['nomor_telp'].widget.attrs.update({'class': 'form-control','placeholder': 'Nomor Telepon Pembeli'})
        self.fields['catatan'].widget.attrs.update({'class': 'form-control','placeholder': 'Catatan'})
            
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
    
class ListPesananForm(forms.ModelForm):
    class Meta:
        model = ListPesanan
        fields = ['pesanan', 'barang_jadi', 'jumlah_barang_jadi']
