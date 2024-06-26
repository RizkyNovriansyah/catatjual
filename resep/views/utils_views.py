# views.py
from ..models import ResepBahanJadi, MasterBahan, ResepOlahanJadi, BahanOlahan, ResepBahanOlahan
from django.views.generic.base import TemplateView

class ErrorPageView(TemplateView):
    template_name = 'error_page.html'  # Ganti 'error_page.html' dengan nama template halaman error Anda

def add_resep_to_olah(olahan,list_bahans):
    for bahan in list_bahans:
        kode_bahan = bahan['id'].split("#")[1]
        mb = MasterBahan.objects.get(kode_bahan=kode_bahan)
        rbo = ResepBahanOlahan.objects.create(
            bahan_olahan = olahan,
            master_bahan = mb,
            jumlah_pemakaian = bahan['value']
        )
        rbo.save()

def add_resep_to_jadi(barang_jadi, list_bahans):
    for bahan in list_bahans:
        tipe = bahan['id'].split("_")[0]
        kode_bahan = bahan['id'].split("#")[1]
        if tipe == "bahan":
            mb = MasterBahan.objects.get(kode_bahan=kode_bahan)
            rbo = ResepBahanJadi.objects.create(
                barang_jadi=barang_jadi,
                master_bahan=mb,
                jumlah_pemakaian=bahan['value']
            )
            rbo.save()
        elif tipe == "olahan":
            id_olahan = kode_bahan.split("_")[1]
            bo = BahanOlahan.objects.get(id=id_olahan)
            roj = ResepOlahanJadi.objects.create(
                barang_jadi=barang_jadi,
                bahan_olahan=bo,
                jumlah_pemakaian=bahan['value']
            )
            roj.save()

def get_bahan_used(barang_jadi):
    daftar_resep_bahan = ResepBahanJadi.objects.filter(barang_jadi=barang_jadi)
    bahan_used_list = []
    for item in daftar_resep_bahan:
        bahan_used_list.append({
            'id': item.id,
            'master_bahan_id': item.master_bahan.id,
            'barang_jadi_id': item.barang_jadi.id,
            'jumlah_pemakaian': item.jumlah_pemakaian,
            'is_deleted': str(item.is_deleted).lower()  # Convert boolean to lowercase string
        })

    return bahan_used_list

def get_olahan_used(barang_jadi):
    daftar_resep_olahan = ResepOlahanJadi.objects.filter(barang_jadi=barang_jadi)
    olahan_used_list = []
    for item in daftar_resep_olahan:
        olahan_used_list.append({
            'id': item.id,
            'bahan_olahan_id': item.bahan_olahan.id,
            'barang_jadi_id': item.barang_jadi.id,
            'jumlah_pemakaian': item.jumlah_pemakaian,
            'is_deleted': str(item.is_deleted).lower()  # Convert boolean to lowercase string
        })

    return olahan_used_list
    
    