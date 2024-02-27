# views.py
from django.shortcuts import render, redirect
from .models import Resep, MasterBahan, BarangJadi
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
        # get tes
        # tes = request.POST.get('tes')
        # print('tes:', tes)
        # MasterBahan.objects.create(
        #     name=request.POST.get('name'),
        #     total=request.POST.get('total'),
        #     qty_keseluruhan=request.POST.get('qty_keseluruhan'),
        #     qty_terkecil=request.POST.get('qty_terkecil'),
        # )
        form = MasterBahanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bahan_list')
    else:
        form = MasterBahanForm()
    return render(request, 'resep/bahan_form.html', locals())

def bahan_detail(request, pk):
    bahan = MasterBahan.objects.get(pk=pk)
    return render(request, 'resep/bahan_detail.html', {'bahan': bahan})

# RESEP ROTI
def resep_list(request):
    # resep = Resep.objects.all()
    # print("resep",resep)
    barang_jadi = BarangJadi.objects.all()
    print("barang_jadi",barang_jadi)
    return render(request, 'resep/resep_list.html', locals())


def resep_create(request):
    bahans = MasterBahan.objects.filter(is_deleted=False)
    

    if request.method == 'POST':
        # get bahans array 
        nama = request.POST.get('nama')
        kode_barang = request.POST.get('kode_barang')
        harga_jual = request.POST.get('harga_jual')
        bahan_digunakan = request.POST.getlist('bahans') # yang kepake
        bahans_id = request.POST.getlist('bahans_id')
        bahans_jumlah = request.POST.getlist('bahans_jumlah')
        
        print('bahan:', bahan_digunakan)
        print('bahans_id:', bahans_id)
        print('bahans_jumlah:', bahans_jumlah)

        barang_jadi = BarangJadi.objects.create(
            nama=nama,
            harga_jual=harga_jual,
            kode_barang=kode_barang
        )
        print("barang_jadi",barang_jadi)
        
        index = 0
        total_hpp = 0
        for bahan_jumlah in bahans_jumlah:
            if bahan_jumlah != '':
                print('bahan_jumlah:', bahan_jumlah)
                print('bahan_id:', bahans_id[index])
                
                # print('bahan:', bahan)
                bahan = MasterBahan.objects.get(id=bahans_id[index])
                harga_per_bahan = bahan.qty_terkecil
                total_hpp += int(harga_per_bahan)

                r = Resep.objects.create(
                    master_bahan=bahan,
                    barang_jadi=barang_jadi,
                    jumlah_pemakaian=bahan_jumlah
                )
                print("resep",r.id)
                index += 1       

        barang_jadi.hpp = total_hpp
        barang_jadi.save()
        redirect('resep_list')
        
    else:
        form = ResepForm()

    
    return render(request, 'resep/resep_form.html', locals())

def resep_detail(request, pk):
    barang_jadi = BarangJadi.objects.get(pk=pk)
    reseps = Resep.objects.filter(barang_jadi=barang_jadi)
    
    return render(request, 'resep/resep_detail.html', locals())

# def resep_detail(request, pk):
#     resep = Resep.objects.get(pk=pk)
#     bahan = resep.resep.all()
#     return render(request, 'resep/resep_detail.html', {'resep': [resep], 'resep_all': resep, 'bahan': bahan})

# def resep_detail(request, pk):
#     resep = Resep.objects.get(pk=pk)
#     return render(request, 'resep/resep_detail.html', {'resep': resep})