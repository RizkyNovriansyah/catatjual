# vim: set fileencoding=utf-8 :
from django.contrib import admin

import resep.models as models

class BarangJadiAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'nama',
        'kode_barang',
        'harga_jual',
        'daftar_bahan',
        'hpp',
        'is_deleted',
        'master_roti',
    )
    list_filter = (
        'is_deleted',
        'master_roti',
        'id',
        'nama',
        'kode_barang',
        'harga_jual',
        'daftar_bahan',
        'hpp',
    )


class MasterBahanAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'kode_bahan',
        'nama',
        'total',
        'qty_keseluruhan',
        'qty_terkecil',
        'harga',
        'harga_jual',
        'harga_kg',
        'harga_gram',
        'created_date',
        'updated_date',
        'is_deleted',
    )
    list_filter = (
        'created_date',
        'updated_date',
        'is_deleted',
        'id',
        'kode_bahan',
        'nama',
        'total',
        'qty_keseluruhan',
        'qty_terkecil',
        'harga',
        'harga_jual',
        'harga_kg',
        'harga_gram',
    )


class ResepAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'master_bahan',
        'barang_jadi',
        'jumlah_pemakaian',
        'is_deleted',
    )
    list_filter = (
        'master_bahan',
        'barang_jadi',
        'is_deleted',
        'id',
        'jumlah_pemakaian',
    )


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.BarangJadi, BarangJadiAdmin)
_register(models.MasterBahan, MasterBahanAdmin)
_register(models.Resep, ResepAdmin)
