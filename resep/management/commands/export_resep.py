import csv
from django.core.management.base import BaseCommand
from resep.models import BarangJadi, ListPesanan, MasterBahan, Pesanan, Resep
import pandas as pd
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Export data from database to an Excel file'

    def handle(self, *args, **kwargs):
        # Export data from Pesanan model
        # pesanan_data = list(Pesanan.objects.values())
        # df_pesanan = pd.DataFrame(pesanan_data)
        # df_pesanan.to_excel('pesanan.xlsx', index=False)

        # Export data from ListPesanan model
        # list_pesanan_data = list(ListPesanan.objects.values())
        # df_list_pesanan = pd.DataFrame(list_pesanan_data)
        # df_list_pesanan.to_excel('list_pesanan.xlsx', index=False)

        # Export data from BarangJadi model
        barang_jadi_data = list(BarangJadi.objects.values())
        df_barang_jadi = pd.DataFrame(barang_jadi_data)
        df_barang_jadi.to_excel('barang_jadi.xlsx', index=False)

        # Export data from MasterBahan model
        # master_bahan_data = list(MasterBahan.objects.values())
        # df_master_bahan = pd.DataFrame(master_bahan_data)
        # df_master_bahan.to_excel('master_bahan.xlsx', index=False)

        # Export data from Resep model
        resep_data = list(Resep.objects.values())
        df_resep = pd.DataFrame(resep_data)
        df_resep.to_excel('resep.xlsx', index=False)

        self.stdout.write(self.style.SUCCESS('Data has been exported to Excel files successfully.'))
