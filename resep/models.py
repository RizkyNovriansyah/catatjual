# models.py
from django.db import models

class Resep(models.Model):
    nama = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nama

class Bahan(models.Model):
    nama = models.CharField(max_length=100)
    resep = models.ManyToManyField(Resep)
    harga = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nama
