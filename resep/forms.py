# forms.py
from django import forms
from .models import Roti, Penjualan, BahanBaku, KomposisiRoti

class RotiForm(forms.ModelForm):
    bahan_baku = forms.ModelMultipleChoiceField(queryset=BahanBaku.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Roti
        fields = '__all__'

class PenjualanForm(forms.ModelForm):
    class Meta:
        model = Penjualan
        fields = ['roti', 'jumlah', 'harga_jual']

class BahanBakuForm(forms.ModelForm):
    class Meta:
        model = BahanBaku
        fields = '__all__'
