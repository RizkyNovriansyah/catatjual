# views.py
from django.shortcuts import render, redirect
from .models import Resep, Bahan
from .forms import ResepForm, BahanForm
from django.db.models import Sum

def index(request):
    pesanans = []
    return render(request, 'index.html', locals())

# BAHAN ROTI
def bahan_list(request):
    bahans = Bahan.objects.all()
    return render(request, 'resep/bahan_list.html', {'bahans': bahans})

def bahan_create(request):
    if request.method == 'POST':
        form = BahanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bahan_list')
    else:
        form = BahanForm()
    return render(request, 'resep/bahan_form.html', {'form': form})

def bahan_detail(request, pk):
    bahan = Bahan.objects.get(pk=pk)
    return render(request, 'resep/bahan_detail.html', {'bahan': bahan})

# RESEP ROTI
def resep_list(request):
    categories = Resep.objects.all()
    return render(request, 'resep/resep_list.html', {'categories': categories})


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
    total_price = resep.bahan_set.aggregate(total_price=Sum('price'))['total_price'] or 0
    return render(request, 'resep/resep_detail.html', {'resep': resep, 'total_price': total_price})

