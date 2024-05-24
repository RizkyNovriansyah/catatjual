# Inisialisasi grup di Django shell atau dalam script terpisah
from django.contrib.auth.models import Group, Permission
from catat.models import UserProfile



# Membuat grup
admin_group, created = Group.objects.get_or_create(name='Admin')
karyawan_group, created = Group.objects.get_or_create(name='Karyawan')

# Menambahkan user ke grup
#admin
user_admin = UserProfile.objects.get(email='admin@admin.com')
admin_group.user_set.add(user_admin)

#karyawan
user_karyawan = UserProfile.objects.get(email='karyawan@karyawan.com')
karyawan_group.user_set.add(user_karyawan)
