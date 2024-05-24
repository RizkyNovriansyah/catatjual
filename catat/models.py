# accounts/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission, User
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(password, username, **extra_fields)

# class User(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=100, unique=True, blank=False, null=False)
#     daily_login = models.DateTimeField(auto_now_add=False, null=True, blank=True)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     groups = models.ManyToManyField( Group, related_name='groups_user_set',  blank=True,)
#     user_permissions = models.ManyToManyField(Permission, related_name='permissions_user_set', blank=True,)
    
#     objects = CustomUserManager()
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = []
#     def __str__(self):
#         return self.username
    
class LoginSessionsTrack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    daily_login = models.DateTimeField(auto_now_add=False, null=True, blank=True)