# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission, User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Menghapus semua validator untuk password1
        self.fields['password1'].validators = []

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        try:
            # Melakukan validasi password kosong untuk memastikan password tidak kosong
            validate_password(password1, self.instance)
        except ValidationError as error:
            # Jika ada kesalahan validasi, tampilkan pesan kesalahan yang sesuai
            self.add_error('password1', error)
        return password1

class UserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Menghapus semua validator untuk password1
        self.fields['password1'].validators = []

    class Meta:
        model = User
        fields = ('username',)
