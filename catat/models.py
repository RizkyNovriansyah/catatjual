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

class LoginSessionsTrack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    daily_login = models.DateTimeField(auto_now_add=False, null=True, blank=True)