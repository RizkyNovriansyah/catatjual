import openpyxl
from django.core.management.base import BaseCommand
from resep.models import BarangJadi, MasterBahan, Resep

class Command(BaseCommand):
    help = 'Import data from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        
        # Load the workbook
        workbook = openpyxl.load_workbook(file_path)
        
        # Assuming the data is in the first two sheets as per export mechanism
        worksheet_barang_jadi = workbook["Barang Jadi"]
        worksheet_resep = workbook["Resep"]
        
        # Process data for Barang Jadi
        for row in worksheet_barang_jadi.iter_rows(min_row=2, values_only=True):
            barang_jadi = BarangJadi.objects.create(
                nama=row[0],
                kode_barang=row[1],
                harga_jual=row[2],
                hpp=row[3],
                master_bahan=row[4]
            )
        
        # Process data for Resep
        for row in worksheet_resep.iter_rows(min_row=2, values_only=True):
            barang_jadi = BarangJadi.objects.get(kode_barang=row[0])  # Assuming kode_barang is unique
            master_bahan = MasterBahan.objects.get(kode_bahan=row[4])  # Assuming kode_bahan is unique
            Resep.objects.create(
                barang_jadi=barang_jadi,
                master_bahan=master_bahan,
                jumlah_pemakaian=row[2],
            )

        self.stdout.write(self.style.SUCCESS('Import data done!'))
