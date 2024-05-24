
# catatjual

1. Clone repository:
   git clone -b dev-crud https://github.com/RizkyNovriansyah/catatjual.git

2. Pull latest changes:
   git pull origin dev-crud

3. Install requirements:
   pip install -r requirements.txt

4. Run migrations:
   python manage.py migrate

5. Import bahan CSV:
   python manage.py import_bahan

6. Delete all bahan:
   python manage.py delete_bahan

7. Import Resep dilakukan setelah import bahan
   python manage.py import_resep "Lokasi File excel"/import_resep.xlsx
   Example :
   python manage.py import_resep /home/enigma/code/github/catatjual/import_resep.xlsx

8. Export Resep
   python manage.py export_resep
   file excel disimpan pada folder data
   Example :
   Export Resep done! File saved at: data/export_resep_2024-05-14.xlsx