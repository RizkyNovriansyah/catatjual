from django.shortcuts import render
import json
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.db.models.query import QuerySet
from django.views import View  
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from resep.models import BarangJadi, MasterBahan, Resep
from pesan.models import ListPesanan, Pesanan
from django.urls import reverse_lazy
from django.views import generic
from .forms import UserProfileCreationForm
from catat.models import LoginSessionsTrack, UserProfile
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.utils import timezone

from django.utils import timezone
from datetime import timedelta

class LoginView(LoginView):
    template_name = 'registration/login.html' 

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        self.update_login_time(user)
        return HttpResponseRedirect(self.get_success_url())

    def update_login_time(self, user):
        login_track, created = LoginSessionsTrack.objects.get_or_create(user=user)
        login_track.daily_login = timezone.now()
        login_track.save()

    def get_login_info(self, user):
        login_track = LoginSessionsTrack.objects.filter(user=user).first()
        if login_track:
            login_time = timezone.now() - login_track.daily_login
            return int(login_time.total_seconds() / 60)  # Menghitung menit
        return 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[REDIRECT_FIELD_NAME] = self.request.GET.get(REDIRECT_FIELD_NAME, '')
        if self.request.user.is_authenticated:
            login_info = self.get_login_info(self.request.user)
            context['login_info'] = login_info
        return context

    
def dashboard(request):
    barang_jadi_count = BarangJadi.objects.filter(is_deleted=False).count()
    resep_count = Resep.objects.filter(is_deleted=False).count()
    bahan_count = MasterBahan.objects.filter(is_deleted=False).count()
    list_pesanan_count = ListPesanan.objects.filter(is_deleted=False).count()
    
    email = ''
    login_info = 0  

    if request.user.is_authenticated:
        email = request.user.email
        login_track = LoginSessionsTrack.objects.filter(user=request.user).first()
        if login_track:
            login_time = timezone.now() - login_track.daily_login
            login_info = int(login_time.total_seconds() / 60)  # Menghitung menit
            print('login_info: ', login_info)
    
    context = {'bahan_count': bahan_count,
               'resep_count': resep_count,
               'email': email,
               'login_info': login_info,  # Menambahkan login_info ke dalam konteks
               'list_pesanan_count': list_pesanan_count,
               'barang_jadi_count': barang_jadi_count}
    return render(request, 'dashboard.html', context)

def profile(request):
    user = UserProfile.objects.get(email=request.user)
    
    
    context = {'user': user,
                'email' : user.email, 
                'is_staff' : user.is_staff, 
                'is_active' : user.is_active, 
                'date_joined' : user.date_joined, 
                'groups' : user.groups,
                'user_permissions': user.user_permissions,
               }
    return render(request, 'profile.html', context)





    
class SignUpView(generic.CreateView):
    form_class = UserProfileCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    
