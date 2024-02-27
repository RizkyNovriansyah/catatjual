# models.py
from django.utils import timezone
from django.db import models

class Pesanan(models.Model):
    nama = models.CharField(max_length=100)
    alamat = models.TextField(max_length=100)
    
    
class ListPesanan(models.Model):
    Pesanan = models.ForeignKey(Pesanan)
    BarangJadi = models.CharField(max_length=100, blank=True, null=True)
    jumlah_barang_jadi = models.IntegerField(blank=True, null=True, default=0)    

class BarangJadi(models.Model):
    nama = models.CharField(max_length=100, blank=True, null=True)
    kode_barang = models.CharField(max_length=100, blank=True, null=True)
    harga_jual = models.IntegerField(blank=True, null=True)
    hpp = models.IntegerField(blank=True, null=True)
    
class Resep(models.Model):
    nama = models.CharField(max_length=100, blank=True, null=True)
    kode_barang = models.CharField(max_length=100, blank=True, null=True)
    Barang_jadi = models.ForeignKey(BarangJadi)
    master_bahan = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.nama

    
    
class MasterBahan(models.Model):
    kode_bahan = models.CharField(max_length=100,blank=True, null=True)
    nama = models.CharField(max_length=100, blank=True, null=True)
    resep = models.ManyToManyField(Resep)
    total = models.CharField(max_length=100, blank=True, null=True)
    qty_keseluruhan = models.IntegerField(blank=True, null=True, default=0)
    qty_terkecil = models.IntegerField(blank=True, null=True, default=0)
    harga = models.IntegerField(blank=True, null=True, default=0)
    harga_jual = models.IntegerField(blank=True, null=True, default=0)
    harga_kg = models.IntegerField(blank=True, null=True, default=0)    #harga_perkg
    harga_gram = models.IntegerField(blank=True, null=True, default=0)  #harga_pergr
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    @property
    def get_created_date(self):
        return timezone.localtime(self.created_date)
    
    @property
    def get_updated_date(self):
        return timezone.localtime(self.updated_date)
    

    def __str__(self):
        return self.nama
