
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

9. Export models to png :
   sudo apt-get install graphviz
   pip install django-extensions
   python manage.py graph_models -a -o new_models.dot
   dot -Tpng new_models.dot -o new_models.png

10. Update requirements.txt
    pip freeze > requirements.txt 

# Deploy
0. persiapan
 - sudo apt update

1. persiapan venv 
 - apt-get install python3-venv  nginx 
 - mkdir venv
 - python3 -m venv venv
2. installing nginx
 - sudo apt install nginx
 - sudo systemctl status nginx
 - sudo systemctl enable nginx
https://www.rumahweb.com/journal/cara-install-django-python-di-vps-ubuntu/