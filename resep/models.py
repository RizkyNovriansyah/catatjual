from django.db import models
from django.contrib.auth.models import User

class BahanBaku(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)
    harga_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stok = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.nama

class Roti(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)
    bahan_baku = models.ManyToManyField(BahanBaku, through='KomposisiRoti')
    harga_jual = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.nama

class KomposisiRoti(models.Model):
    roti = models.ForeignKey(Roti, on_delete=models.CASCADE)
    bahan_baku = models.ForeignKey(BahanBaku, on_delete=models.CASCADE)
    jumlah = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class Penjualan(models.Model):
    roti = models.ForeignKey(Roti, on_delete=models.CASCADE)
    jumlah = models.IntegerField(null=True, blank=True)
    harga_jual = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tanggal_penjualan = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alamat = models.CharField(max_length=200, null=True, blank=True)
    nomor_telepon = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.user.username
