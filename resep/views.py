from django.shortcuts import render, redirect
from .models import Roti, Penjualan, BahanBaku, KomposisiRoti
from .forms import RotiForm, PenjualanForm, BahanBakuForm

# Create your views here.
def index(request):
    pesanans = []
    return render(request, 'index.html', locals())

def tambah_roti(request):
    if request.method == 'POST':
        form = RotiForm(request.POST)
        if form.is_valid():
            roti = form.save()
            bahan_baku_data = form.cleaned_data['bahan_baku']
            for bahan in bahan_baku_data:
                jumlah_key = f'jumlah_{bahan.id}'
                jumlah = request.POST.get(jumlah_key)
                if jumlah:
                    komposisi = KomposisiRoti(roti=roti, bahan_baku=bahan, jumlah=jumlah)
                    komposisi.save()
            return redirect('daftar_roti')
    else:
        form = RotiForm()
    return render(request, 'resep/tambah_roti.html', {'form': form})

def daftar_roti(request):
    roti = Roti.objects.all()
    return render(request, 'resep/daftar_roti.html', {'roti': roti})

def tambah_penjualan(request):
    if request.method == 'POST':
        form = PenjualanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('daftar_penjualan')
    else:
        form = PenjualanForm()
    return render(request, 'resep/tambah_penjualan.html', {'form': form})

def daftar_penjualan(request):
    penjualan = Penjualan.objects.all()
    return render(request, 'resep/daftar_penjualan.html', {'penjualan': penjualan})

def tambah_bahan_baku(request):
    if request.method == 'POST':
        form = BahanBakuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('daftar_bahan_baku')
    else:
        form = BahanBakuForm()
    return render(request, 'resep/tambah_bahan_baku.html', {'form': form})

def daftar_bahan_baku(request):
    bahan_baku = BahanBaku.objects.all()
    return render(request, 'resep/daftar_bahan_baku.html', {'bahan_baku': bahan_baku})
