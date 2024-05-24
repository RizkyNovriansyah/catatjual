# vim: set fileencoding=utf-8 :
from django.contrib import admin

import pesan.models as models


class PesananAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'nama',
        'alamat',
        'pesanan',
        'tanggal_pesan',
        'total_harga',
        'total_bayar',
        'harga_modal',
        'nomor_telp',
        'catatan',
        'created_date',
        'updated_date',
        'is_deleted',
    )
    list_filter = (
        'tanggal_pesan',
        'created_date',
        'updated_date',
        'is_deleted',
        'id',
        'nama',
        'alamat',
        'pesanan',
        'total_harga',
        'total_bayar',
        'harga_modal',
        'nomor_telp',
        'catatan',
    )


class ListPesananAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'pesanan',
        'barang_jadi',
        'jumlah_barang_jadi',
        'created_date',
        'updated_date',
        'is_deleted',
    )
    list_filter = (
        'pesanan',
        'barang_jadi',
        'created_date',
        'updated_date',
        'is_deleted',
        'id',
        'jumlah_barang_jadi',
    )


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Pesanan, PesananAdmin)
_register(models.ListPesanan, ListPesananAdmin)
