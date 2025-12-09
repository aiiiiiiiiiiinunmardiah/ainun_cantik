from django.shortcuts import render,redirect
from .models import Barang
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/`')
def tambah_laundry(request):
    if request.method == 'POST':
        nama = request.POST.get("nama")
        jenis = request.POST.get("jenis")
        berat = request.POST.get("berat")
        harga = request.POST.get("harga")
        status = request.POST.get("status")
        
        Barang.objects.create(nama=nama,jenis=jenis,berat=berat,harga=harga,status=status)
        me = request.user
        if me.is_staff and me.is_superuser:
            return redirect('/daftar_laundry_super/')
        elif me.is_staff:  # bukan superuser, tapi admin
            return redirect('/daftar_laundry_admin/')
        else:
            return redirect('/daftar_laundry_user/')

    return render(request,'tambah_laundry.html')