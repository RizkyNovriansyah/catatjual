import csv
from django.core.management.base import BaseCommand
from resep.models import MasterBahan

class Command(BaseCommand):
    help = 'Import data bahan dari file CSV'

    def handle(self, *args, **options):
        csv_file = 'Bahan.csv.csv'  # Ganti dengan path ke file CSV Anda

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    harga_kg = int(row['Harga Beli']) / int(row['Quantity Keseluruhan'])
                    print('harga_kg: ', harga_kg)
                    harga_gram = harga_kg / int(row['Quantity Terkecil'])
                    print('harga_gram: ', harga_gram)
                except ZeroDivisionError:
                    harga_kg = None  # Atau sesuaikan dengan nilai default yang sesuai
                    harga_gram = None  # Atau sesuaikan dengan nilai default yang sesuai

                bahan = MasterBahan.objects.create(
                    nama=row['Nama Bahan'],
                    kode_bahan=row['Kode Bahan'],
                    qty_keseluruhan=row['Quantity Keseluruhan'],
                    qty_terkecil=row['Quantity Terkecil'],
                    harga=row['Harga Beli'],
                    harga_kg=harga_kg,
                    harga_gram=harga_gram,
                )

                
                bahan.save()

        self.stdout.write(self.style.SUCCESS('Data bahan berhasil diimpor'))

