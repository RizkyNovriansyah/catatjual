# forms.py
from django import forms
from .models import BarangJadi, Resep, MasterBahan
from decimal import Decimal

class ResepForm(forms.ModelForm):
    class Meta:
        model = Resep
        fields = ['master_bahan',
                    'barang_jadi',
                    'jumlah_pemakaian',]

class BarangJadiForm(forms.ModelForm):
    class Meta:
        model = BarangJadi
        fields = ['nama', 'kode_barang', 'hpp', 'harga_jual']

class MasterBahanForm(forms.ModelForm):
    class Meta:
        model = MasterBahan
        fields = ['kode_bahan', 'nama', 'total', 'qty_keseluruhan', 'qty_terkecil', 'harga', 'harga_jual']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kode_bahan'].label = 'Kode Bahan'
        self.fields['nama'].label = 'Nama Bahan'
        self.fields['total'].label = 'total'
        self.fields['qty_keseluruhan'].label = 'qty_keseluruhan'
        self.fields['qty_terkecil'].label = 'qty_terkecil'
        self.fields['harga'].label = 'harga'
        self.fields['harga_jual'].label = 'harga_jual'

        # add css in nama
        self.fields['kode_bahan'].widget.attrs.update({'class':'form-control','placeholder':"GG000"})
        self.fields['nama'].widget.attrs.update({'class':'form-control','placeholder':"Gula"})
        self.fields['total'].widget.attrs.update({'class':'form-control','placeholder':"total"})
        self.fields['qty_keseluruhan'].widget.attrs.update({'class':'form-control','placeholder':"10000"})
        self.fields['qty_terkecil'].widget.attrs.update({'class':'form-control','placeholder':"100"})
        self.fields['harga'].widget.attrs.update({'class':'form-control','placeholder':"500000",'onkeyup':'cek_harga_perkeseluruhan()'})
        self.fields['harga_jual'].widget.attrs.update({'class':'form-control','placeholder':""})

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
        