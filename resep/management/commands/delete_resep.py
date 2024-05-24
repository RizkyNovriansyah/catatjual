from django.core.management.base import BaseCommand
from resep.models import BarangJadi

class Command(BaseCommand):
    help = 'Menghapus semua daftar resep'

    def handle(self, *args, **options):
        # Menghapus semua daftar barang jadi
        deleted_resep = BarangJadi.objects.all()
        for resep in deleted_resep:
            nama_resep = resep.nama
            resep.delete()
            self.stdout.write(self.style.SUCCESS(f'resep {nama_resep} berhasil dihapus'))

        self.stdout.write(self.style.SUCCESS('Semua daftar resep berhasil dihapus'))
