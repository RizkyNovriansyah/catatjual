# forms.py
from django import forms
from .models import Resep, MasterBahan

class ResepForm(forms.ModelForm):
    class Meta:
        model = Resep
        fields = ['nama']

class MasterBahanForm(forms.ModelForm):
    class Meta:
        model = Bahan
        fields = ['nama', 'harga']
