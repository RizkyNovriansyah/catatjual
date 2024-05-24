import glob

from django.contrib.auth.models import Group
from django.core.management import call_command
import os
from django.core.management.base import BaseCommand
from django.db.models import signals
from catat.models import CustomUserManager, User, LoginSessionsTrack


class Command(BaseCommand):
    help = "Command to clean all migrations file of Coofis NDE"

    def handle(self, *args, **options):
        User.objects.create_superuser(username='admin', password='password', email='admin@admin.com')

