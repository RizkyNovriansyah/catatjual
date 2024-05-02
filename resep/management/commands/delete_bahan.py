from django.core.management.base import BaseCommand
from resep.models import MasterBahan

class Command(BaseCommand):
    help = 'Menghapus semua daftar bahan'

    def handle(self, *args, **options):
        # Menghapus semua daftar bahan
        deleted_bahan = MasterBahan.objects.all()
        for bahan in deleted_bahan:
            nama_bahan = bahan.nama
            bahan.delete()
            self.stdout.write(self.style.SUCCESS(f'Bahan {nama_bahan} berhasil dihapus'))

        self.stdout.write(self.style.SUCCESS('Semua daftar bahan berhasil dihapus'))
