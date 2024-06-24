# forms.py
from django import forms
from .models import BarangJadi, ResepBahanJadi, MasterBahan, BahanOlahan
from decimal import Decimal

class ResepForm(forms.ModelForm):
    class Meta:
        model = ResepBahanJadi
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
        self.fields['kode_bahan'].widget.attrs.update({'class':'form-control','placeholder':"contoh : GG000"})
        self.fields['nama'].widget.attrs.update({'class':'form-control','placeholder':"contoh : Gula"})
        self.fields['total'].widget.attrs.update({'class':'form-control','placeholder':"contoh : total"})
        self.fields['qty_keseluruhan'].widget.attrs.update({'class':'form-control check-harga','placeholder':"contoh : 10000"})
        self.fields['qty_terkecil'].widget.attrs.update({'class':'form-control','placeholder':"contoh : 100"})
        self.fields['harga'].widget.attrs.update({'class':'form-control check-harga bantuan-rupiah','placeholder':"contoh : 500000","data-nama-bantuan":"harga-bantuan-rupiah"})
        self.fields['harga_jual'].widget.attrs.update({'class':'form-control check-harga','placeholder':"contoh : "})

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
        
# class BahanOlahan(models.Model):
#     nama = models.CharField(max_length=100, blank=True, null=True)
#     qty_keseluruhan = models.IntegerField(blank=True, null=True, default=0)
#     qty_terkecil = models.IntegerField(blank=True, null=True, default=0)
#     harga_kg = models.IntegerField(blank=True, null=True, default=0)
#     harga_gram = models.IntegerField(blank=True, null=True, default=0)
#     created_date = models.DateTimeField(auto_now_add=True)
#     updated_date = models.DateTimeField(auto_now=True)
#     is_deleted = models.BooleanField(default=False)
#     history = HistoricalRecords()
    
#     def __str__(self):
#         return self.nama

class BahanOlahanForm(forms.ModelForm):

    class Meta:
        model = BahanOlahan
        fields = ['nama', 'qty_keseluruhan', 'qty_terkecil', 'harga_kg', 'harga_gram']
        # add hpp
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nama'].label = 'Nama Bahan'
        self.fields['qty_keseluruhan'].label = 'Qty Keseluruhan'
        self.fields['qty_terkecil'].label = 'Qty Terkecil'
        self.fields['harga_kg'].label = 'Harga per Kg'
        self.fields['harga_gram'].label = 'Harga per Gram'

        # add css in nama
        self.fields['nama'].widget.attrs.update({'class':'form-control','placeholder':"contoh : Gula"})
        self.fields['qty_keseluruhan'].widget.attrs.update({'class':'form-control check-harga','placeholder':"contoh : 10000"})
        self.fields['qty_terkecil'].widget.attrs.update({'class':'form-control','placeholder':"contoh : 100"})
        self.fields['harga_kg'].widget.attrs.update({'class':'form-control check-harga bantuan-rupiah','placeholder':"contoh : 500000","data-nama-bantuan":"harga-bantuan-rupiah"})
        self.fields['harga_gram'].widget.attrs.update({'class':'form-control check-harga','placeholder':"contoh : ", "name":"hpp_input", "id":"hpp_input"})


    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance