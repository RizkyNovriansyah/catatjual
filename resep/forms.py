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

    def clean(self):
        cleaned_data = super().clean()
        hpp = cleaned_data.get('hpp')
        harga_jual = cleaned_data.get('harga_jual')

        # Custom validation logic if needed
        if hpp and harga_jual:
            if hpp > harga_jual:
                raise forms.ValidationError("HPP tidak boleh lebih besar dari Harga Jual")

        return cleaned_data


    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['nama'].label = 'Nama Barang'
            self.fields['kode_barang'].label = 'Kode Barang'
            self.fields['hpp'].label = 'HPP'
            self.fields['harga_jual'].label = 'Harga Jual'

            self.fields['nama'].widget.attrs.update({'class':'form-control','placeholder':"contoh : Roti"})
            self.fields['kode_barang'].widget.attrs.update({'class':'form-control','placeholder':"contoh : RT001"})
            self.fields['hpp'].widget.attrs.update({'class':'form-control d-none','placeholder':"contoh : 5000", "readonly":"readonly"})
            self.fields['harga_jual'].widget.attrs.update({'class':'form-control check-harga bantuan-rupiah','placeholder':"contoh : 5000","data-nama-bantuan":"harga-bantuan-rupiah"})

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

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

class BahanOlahanForm(forms.ModelForm):
    class Meta:
        model = BahanOlahan
        fields = ['nama', 'qty_keseluruhan', 'qty_terkecil', 'total', 'harga']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nama'].label = 'Nama Bahan'
        self.fields['total'].label = 'total'
        self.fields['harga'].label = 'harga'
        self.fields['qty_keseluruhan'].label = 'qty_keseluruhan'
        self.fields['qty_terkecil'].label = 'qty_terkecil'

        # add css in nama
        self.fields['nama'].widget.attrs.update({'class':'form-control','placeholder':"contoh : Gula"})
        self.fields['total'].widget.attrs.update({'class':'form-control','placeholder':"contoh : total"})
        self.fields['harga'].widget.attrs.update({'class':'form-control check-harga bantuan-rupiah','placeholder':"contoh : 500000","data-nama-bantuan":"harga-bantuan-rupiah"})
        self.fields['qty_keseluruhan'].widget.attrs.update({'class':'form-control check-harga','placeholder':"contoh : 10000", "value":"10000"})
        self.fields['qty_terkecil'].widget.attrs.update({'class':'form-control','placeholder':"contoh : 100"})

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

        print("2313")

        # add css in nama
        self.fields['nama'].widget.attrs.update({'class':'form-control','placeholder':"contoh : Gula"})
        self.fields['qty_keseluruhan'].widget.attrs.update({'class':'form-control check-harga','placeholder':"contoh : 10000", "id":"qty_keseluruhan","name":"qty_keseluruhan","onkeyup":"cekhpp()"})
        self.fields['qty_keseluruhan'].initial = None


        self.fields['qty_terkecil'].widget.attrs.update({'class':'form-control','placeholder':"contoh : 100"})
        self.fields['harga_kg'].widget.attrs.update({'class':'form-control check-harga bantuan-rupiah d-none','placeholder':"contoh : 500000","data-nama-bantuan":"harga-bantuan-rupiah","name":"harga_kg_input", "id":"harga_kg_input"})
        self.fields['harga_gram'].widget.attrs.update({'class':'form-control check-harga d-none','placeholder':"contoh : ", "name":"hpp_input", "id":"hpp_input"})


    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance