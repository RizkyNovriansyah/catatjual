from django.urls import path, include
from  .views import *
from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import UserProfileCreationForm

urlpatterns = [
    path('', dashboard, name='dashboard'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', profile, name='profile'),
]