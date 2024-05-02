# models.py
from django.utils import timezone

from django.db import models

class Pesanan(models.Model):
    nama = models.CharField(max_length=100)
    alamat = models.TextField(max_length=100)
    
    
class ListPesanan(models.Model):
    Pesanan = models.ForeignKey(Pesanan, on_delete=models.CASCADE, related_name='Pesanan')
    BarangJadi = models.CharField(max_length=100, blank=True, null=True)
    jumlah_barang_jadi = models.IntegerField(blank=True, null=True, default=0)    

class BarangJadi(models.Model):
    nama = models.CharField(max_length=100, blank=True, null=True)
    kode_barang = models.CharField(max_length=100, blank=True, null=True)
    harga_jual = models.IntegerField(blank=True, null=True)     #tambahkan input ini ke tambah roti baru tidak boleh kurang dari modal
    # daftar_bahan = models.CharField(max_length=100, blank=True, null=True)
    # daftar_bahan = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    daftar_bahan = models.JSONField(blank=True, null=True)
    hpp = models.IntegerField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.nama

class MasterBahan(models.Model):
    kode_bahan = models.CharField(max_length=100,blank=True, null=True)
    nama = models.CharField(max_length=100, blank=True, null=True)
    total = models.CharField(max_length=100, blank=True, null=True)
    qty_keseluruhan = models.IntegerField(blank=True, null=True, default=0) # adalah .... , .... 100 kg
    qty_terkecil = models.IntegerField(blank=True, null=True, default=0) # adalah .... , .... 1000
    harga = models.IntegerField(blank=True, null=True, default=0)
    harga_jual = models.IntegerField(blank=True, null=True, default=0)
    harga_kg = models.IntegerField(blank=True, null=True, default=0)    #harga_perkg
    harga_gram = models.IntegerField(blank=True, null=True, default=0)  #harga_pergr
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nama
    
    @property
    def get_created_date(self):
        return timezone.localtime(self.created_date)
    
    @property
    def get_updated_date(self):
        return timezone.localtime(self.updated_date)

class Resep(models.Model):
    master_bahan = models.ForeignKey(MasterBahan,blank=True, null=True, on_delete=models.CASCADE, related_name='MasterBahan')
    barang_jadi = models.ForeignKey(BarangJadi,blank=True, null=True, on_delete=models.CASCADE, related_name='BarangJadi')
    jumlah_pemakaian = models.IntegerField(blank=True, null=True, default=0)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.master_bahan.nama} - {self.barang_jadi.nama}"
 