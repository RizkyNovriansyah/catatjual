# forms.py
from django import forms
from .models import Resep, MasterBahan
from decimal import Decimal

class ResepForm(forms.ModelForm):
    class Meta:
        model = Resep
        fields = '__all__'

class MasterBahanForm(forms.ModelForm):
    class Meta:
        model = MasterBahan
        fields = ['kode_bahan', 'nama', 'total', 'qty_keseluruhan', 'qty_terkecil', 'harga', 'harga_jual']

    def save(self, commit=True):
        instance = super().save(commit=False)
        harga = instance.harga
        total = instance.total

        if harga and total:
            harga_kg = Decimal(harga) / Decimal(total)
            instance.harga_kg = harga_kg

        if commit:
            instance.save()
        return instance
        
