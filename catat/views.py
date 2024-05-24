from django.shortcuts import render
import json
from django.db.models.query import QuerySet
from django.views import View  
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from resep.models import BarangJadi, MasterBahan, Resep
from pesan.models import ListPesanan, Pesanan
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from catat.models import CustomUser
def dashboard(request):
    barang_jadi_count = BarangJadi.objects.filter(is_deleted=False).count()
    resep_count = Resep.objects.filter(is_deleted=False).count()
    bahan_count = MasterBahan.objects.filter(is_deleted=False).count()
    list_pesanan_count = ListPesanan.objects.filter(is_deleted=False).count()
    
    user = request.user
    email = CustomUser.objects.get(email=user)
    
    context = {'bahan_count': bahan_count,
               'resep_count': resep_count,
               'email': email,
               'list_pesanan_count': list_pesanan_count,
               'barang_jadi_count': barang_jadi_count}
    return render(request, 'dashboard.html', context)

def profile(request):
    user = CustomUser.objects.get(email=request.user)
    
    
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
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    
