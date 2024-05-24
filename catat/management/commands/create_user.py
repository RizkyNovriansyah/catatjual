# Inisialisasi grup di Django shell atau dalam script terpisah
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission, User



# Membuat grup
admin_group, created = Group.objects.get_or_create(name='Admin')
karyawan_group, created = Group.objects.get_or_create(name='Karyawan')

# Menambahkan user ke grup
#admin
user_admin = User.objects.get(username='usenrmae')
admin_group.user_set.add(user_admin)

#karyawan
user_karyawan = User.objects.get(username='usenrmae')
karyawan_group.user_set.add(user_karyawan)
