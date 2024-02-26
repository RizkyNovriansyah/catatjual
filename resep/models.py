# models.py
from django.db import models

class Bahan(models.Model):
    nama = models.CharField(max_length=100, blank=False, null=False)
    harga = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)

    def __str__(self):
        return self.nama

class Resep(models.Model):
    nama = models.CharField(max_length=100, blank=False, null=False)
    bahan = models.ManyToManyField(Bahan, related_name='bahan_resep', blank=False, null=False)
    
    def __str__(self):
        return self.nama
