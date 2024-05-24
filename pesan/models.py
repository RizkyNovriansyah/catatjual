# models.py
from django.utils import timezone
from resep.models import BarangJadi, MasterBahan, Resep
from django.db import models

class Pesanan(models.Model):
    nama = models.CharField(max_length=100, blank=True, null=True)
    alamat = models.TextField(max_length=100, blank=True, null=True)
    pesanan = models.JSONField()
    tanggal_pesan = models.DateTimeField(default=timezone.now)
    total_harga = models.IntegerField(default=0)
    total_bayar = models.IntegerField(default=0)
    harga_modal = models.IntegerField(default=0)
    nomor_telp = models.CharField(max_length=100, blank=True, null=True)
    catatan = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.nama

class ListPesanan(models.Model):
    pesanan = models.ForeignKey(Pesanan, on_delete=models.CASCADE, related_name='list_pesanan')
    barang_jadi = models.ForeignKey(BarangJadi, on_delete=models.CASCADE)
    jumlah_barang_jadi = models.IntegerField(default=0)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.pesanan.nama} - {self.barang_jadi.nama}"
    