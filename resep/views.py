# views.py
from django.shortcuts import render, redirect
from .models import Resep, MasterBahan
from .forms import ResepForm, MasterBahanForm
from django.db.models import Sum

def index(request):
    pesanans = []
    return render(request, 'index.html', locals())

# BAHAN ROTI
def bahan_list(request):
    bahans = MasterBahan.objects.all()
    return render(request, 'resep/bahan_list.html', {'bahans': bahans})

def bahan_create(request):
    if request.method == 'POST':
        form = MasterBahanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bahan_list')
    else:
        form = MasterBahanForm()
    return render(request, 'resep/bahan_form.html', {'form': form})

def bahan_detail(request, pk):
    bahan = MasterBahan.objects.get(pk=pk)
    return render(request, 'resep/bahan_detail.html', {'bahan': bahan})

# RESEP ROTI
def resep_list(request):
    resep = Resep.objects.all()
    return render(request, 'resep/resep_list.html', {'resep': resep})


def resep_create(request):
    if request.method == 'POST':
        form = ResepForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bahan_create')
    else:
        form = ResepForm()
    return render(request, 'resep/resep_form.html', {'form': form})

def resep_detail(request, pk):
    resep = Resep.objects.get(pk=pk)
    # Ambil bahan yang terhubung dengan resep tertentu
    bahan = resep.resep.all()
    return render(request, 'resep/resep_detail.html', {'resep': [resep], 'resep_all': resep, 'bahan': bahan})

def resep_detail(request, pk):
    resep = Resep.objects.get(pk=pk)
    bahan = resep.resep.all()
    return render(request, 'resep/resep_detail.html', {'resep': [resep], 'resep_all': resep, 'bahan': bahan})

# def resep_detail(request, pk):
#     resep = Resep.objects.get(pk=pk)
#     return render(request, 'resep/resep_detail.html', {'resep': resep})