from django.core.management.base import BaseCommand
from resep.models import MasterBahan, BahanOlahan

class Command(BaseCommand):
    help = 'Remake sure HPP and Harga Jual for all Barang Jadi and Master Bahan'

    def handle(self, *args, **options):
        
        for mb in MasterBahan.objects.all():
            harga = mb.harga
            quantity = mb.qty_keseluruhan
            if quantity is None or quantity == 0:
                quantity = 1
            harga_gram = float(harga / quantity)
            
            mb.harga_gram = harga_gram

            mb.save()

        for bo in BahanOlahan.objects.all():
            try:
                print(bo)
                harga = bo.harga_kg
                print(harga)
                quantity = bo.qty_keseluruhan
                print(quantity)
                if quantity is None or quantity == 0:
                    quantity = 1
                    bo.qty_keseluruhan = 1
                harga_gram = float(harga / quantity)
                print(harga_gram)
                
                bo.harga_gram = harga_gram

                bo.save()
            except Exception as e:
                print(e)
                pass
    