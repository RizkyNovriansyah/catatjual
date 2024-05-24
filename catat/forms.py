# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile

class UserProfileCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = ('email', 'username')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].validators = []
        self.fields['password2'].validators = []

class UserProfileChangeForm(UserChangeForm):
    class Meta:
        model = UserProfile
        fields = ('email','username')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].validators = []
        self.fields['password2'].validators = []
