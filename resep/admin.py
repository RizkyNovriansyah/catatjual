# vim: set fileencoding=utf-8 :
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
import resep.models as models

class BarangJadiAdmin(SimpleHistoryAdmin):
    list_display = (
        'id',
        'nama',
        'kode_barang',
        'harga_jual',
        'daftar_bahan',
        'hpp',
        'is_deleted',
    )
    list_filter = (
        'is_deleted',
        'id',
        'nama',
        'kode_barang',
        'harga_jual',
        'hpp',
    )


class MasterBahanAdmin(SimpleHistoryAdmin):
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


class BahanOlahanAdmin(SimpleHistoryAdmin):
    list_display = (
        'id',
        'nama',
        'qty_keseluruhan',
        'qty_terkecil',
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
        'nama',
        'qty_keseluruhan',
        'qty_terkecil',
        'harga_kg',
        'harga_gram',
    )


class ResepBahanJadiAdmin(SimpleHistoryAdmin):
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


class ResepOlahanJadiAdmin(SimpleHistoryAdmin):
    list_display = (
        'id',
        'bahan_olahan',
        'barang_jadi',
        'created_date',
        'updated_date',
        'is_deleted',
    )
    list_filter = (
        'created_date',
        'updated_date',
        'is_deleted',
        'id',
        'bahan_olahan',
        'barang_jadi',
    )


admin.site.register(models.BarangJadi, BarangJadiAdmin)
admin.site.register(models.MasterBahan, MasterBahanAdmin)
admin.site.register(models.BahanOlahan, BahanOlahanAdmin)
admin.site.register(models.ResepBahanJadi, ResepBahanJadiAdmin)
admin.site.register(models.ResepOlahanJadi, ResepOlahanJadiAdmin)
