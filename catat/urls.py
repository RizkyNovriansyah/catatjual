from django.urls import path, include
from  .views import *
from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import UserCreationForm
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission, User

urlpatterns = [
    path('', dashboard, name='dashboard'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', profile, name='profile'),
]