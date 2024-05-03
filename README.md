
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
