from django.utils import timezone
from simple_history.models import HistoricalRecords
from django.db import models

class BarangJadi(models.Model):
    nama = models.CharField(max_length=100, blank=True, null=True)
    kode_barang = models.CharField(max_length=100, blank=True, null=True)
    harga_jual = models.IntegerField(blank=True, null=True)
    daftar_bahan = models.JSONField(blank=True, null=True)
    hpp = models.DecimalField(blank=True, null=True, max_digits=60, decimal_places=2)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.nama

class MasterBahan(models.Model):
    kode_bahan = models.CharField(max_length=100, blank=True, null=True)
    nama = models.CharField(max_length=100, blank=True, null=True)
    total = models.CharField(max_length=100, blank=True, null=True)
    qty_keseluruhan = models.IntegerField(blank=True, null=True, default=0)
    qty_terkecil = models.IntegerField(blank=True, null=True, default=0)
    harga = models.IntegerField(blank=True, null=True, default=0)
    harga_jual = models.IntegerField(blank=True, null=True, default=0)
    harga_kg = models.IntegerField(blank=True, null=True, default=0)
    harga_gram = models.DecimalField(blank=True, null=True, max_digits=60, decimal_places=2) # hpp
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.nama
    
    @property
    def get_created_date(self):
        return timezone.localtime(self.created_date)
    
    @property
    def get_updated_date(self):
        return timezone.localtime(self.updated_date)

class ResepBahanJadi(models.Model):
    master_bahan = models.ForeignKey(MasterBahan, blank=True, null=True, on_delete=models.CASCADE, related_name='resep_bahanjadi_bahan')
    barang_jadi = models.ForeignKey(BarangJadi, blank=True, null=True, on_delete=models.CASCADE, related_name='resep_bahanjadi_jadi')
    jumlah_pemakaian = models.IntegerField(blank=True, null=True, default=0)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.master_bahan.nama} - {self.barang_jadi.nama}"

class BahanOlahan(models.Model):
    nama = models.CharField(max_length=100, blank=True, null=True)
    qty_keseluruhan = models.IntegerField(blank=True, null=True, default=0)
    qty_terkecil = models.IntegerField(blank=True, null=True, default=0)
    harga_kg = models.IntegerField(blank=True, null=True, default=0)
    harga_gram = models.DecimalField(blank=True, null=True, max_digits=60, decimal_places=2)
    harga = models.DecimalField(blank=True, null=True, max_digits=60, decimal_places=2)
    total = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.nama

class ResepOlahanJadi(models.Model):
    bahan_olahan = models.ForeignKey(BahanOlahan, on_delete=models.CASCADE, related_name='resep_olahanjadi_olahan')
    barang_jadi = models.ForeignKey(BarangJadi, blank=True, null=True, on_delete=models.CASCADE, related_name='resep_olahanjadi_jadi')
    jumlah_pemakaian = models.IntegerField(blank=True, null=True, default=0)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.barang_jadi.nama} - {self.bahan_olahan.nama}"


class ResepBahanOlahan(models.Model):
    master_bahan = models.ForeignKey(MasterBahan, blank=True, null=True, on_delete=models.CASCADE, related_name='resep_bahanolahan_bahan')
    bahan_olahan = models.ForeignKey(BahanOlahan, blank=True, null=True, on_delete=models.CASCADE, related_name='resep_bahanolahan_olahan')
    jumlah_pemakaian = models.IntegerField(blank=True, null=True, default=0)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.master_bahan.nama} - {self.bahan_olahan.nama}"
