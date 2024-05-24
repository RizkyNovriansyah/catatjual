from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission, User
from catat.models import CustomUserManager

# vim: set fileencoding=utf-8 :
from django.contrib import admin

import catat.models as models


class LoginSessionsTrackAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'daily_login')
    list_filter = ('user', 'daily_login', 'id')


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.LoginSessionsTrack, LoginSessionsTrackAdmin)
