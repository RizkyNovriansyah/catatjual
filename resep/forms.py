# forms.py
from django import forms
from .models import Resep, Bahan

class ResepForm(forms.ModelForm):
    class Meta:
        model = Resep
        fields = ['nama']

class BahanForm(forms.ModelForm):
    class Meta:
        model = Bahan
        fields = ['nama', 'harga']
