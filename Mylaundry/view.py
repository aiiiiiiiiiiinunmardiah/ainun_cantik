from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
import re
from django.contrib import messages
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from data_laundry.models import Barang
from django.core.mail import send_mail
from otp.models import OTP

def My_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            request.session['temp_user_id'] = user.id

            otp_obj, created = OTP.objects.get_or_create(user=user)
            otp_obj.generate()

            send_mail(
                'Kode OTP Login Anda',
                f'Kode OTP: {otp_obj.code}',
                'ainunmrdh015@gmail.com',
                [user.email],
                fail_silently=False
            )

            return redirect('/isi/otp/')

        messages.error(request, "Username atau password salah")
        return redirect('/login/')

    return render(request, 'login.html')

def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
       
        if not re.match(r"^[A-Za-z0-9_]+$", username):
            messages.error(request, "Data tidak valid.")
            return redirect("/register")
        
        if not re.match(r'^[\w_]+@gmail\.com$', email):
            messages.error(request, "Data tidak valid.")
            return redirect("/register") 
        
        try:
            validate_password(password)
        except ValidationError as e:
            msgs = list(e.messages)
            messages.error(request, f"Kata sandi tidak memenuhi aturan: {msgs[0]}")
            return redirect("/register")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Pendaftaran gagal. Periksa data Anda.")
            return redirect("/register")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_staff = False
        user.is_superuser = False
        user.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("/login")
    return render(request,'register.html')

def register_admin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
       
        if not re.match(r"^[A-Za-z0-9_]+$", username):
            messages.error(request, "Data tidak valid.")
            return redirect("/register")
        
        if not re.match(r'^[\w_]+@gmail\.com$', email):
            messages.error(request, "Data tidak valid.")
            return redirect("/register") 
        
        try:
            validate_password(password)
        except ValidationError as e:
            msgs = list(e.messages)
            messages.error(request, f"Kata sandi tidak memenuhi aturan: {msgs[0]}")
            return redirect("/register")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Pendaftaran gagal. Periksa data Anda.")
            return redirect("/register")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_staff = True
        user.is_superuser = False
        user.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("/login")
        
    return render(request,'register.html')
def register_super_admin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
       
        if not re.match(r"^[A-Za-z0-9_]+$", username):
            messages.error(request, "Data tidak valid.")
            return redirect("/register")
        
        if not re.match(r'^[\w_]+@gmail\.com$', email):
            messages.error(request, "Data tidak valid.")
            return redirect("/register") 
        
        try:
            validate_password(password)
        except ValidationError as e:
            msgs = list(e.messages)
            messages.error(request, f"Kata sandi tidak memenuhi aturan: {msgs[0]}")
            return redirect("/register")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Pendaftaran gagal. Periksa data Anda.")
            return redirect("/register")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_superuser = True
        user.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("/login")
    
        
    return render(request,'register.html')

def Mylog_out(request):
    request.session["login_attempts"] = 0
    auth_logout(request)
    return redirect("/login/")


@login_required(login_url='/login')
def daftar_laundry_user(request):
    data = Barang.objects.all()
    return render(request,"daftar_laundry_user.html",{"data" : data})

@login_required(login_url='/login')
def daftar_laundry_admin(request):
    data = Barang.objects.all()
    return render(request,"daftar_laundry_admin.html",{"data" : data})

@login_required(login_url='/login')
def daftar_laundry_super(request):
    data = Barang.objects.all()
    return render(request,"daftar_laundry_super.html",{"data" : data})

def test_email(request,email):
    send_mail(
        'Test OTP',
        'Ini test OTP dari Django',
        'ainunmrdh015@gmail.com',
        [email]
    )

def edit_barang(request, id):
    barang = get_object_or_404(Barang, id=id)

    if request.method == "POST":
        barang.nama = request.POST.get("nama")
        barang.jenis = request.POST.get("jenis")
        barang.berat = request.POST.get("berat")
        barang.status = request.POST.get("status")
        barang.save()
        
        if (request.user.is_superuser):
            return redirect('/daftar_laundry_super/')
        elif (request.user.is_staff):
            return redirect('/daftar_laundry_admin/')

    return render(request, 'edit.html', {"barang": barang})

def hapus_barang(request,id):
    barang = get_object_or_404(Barang,id=id)
    barang.delete()
    if (request.user.is_superuser):
        return redirect('/daftar_laundry_super/')
    elif (request.user.is_staff):
        return redirect('/daftar_laundry_admin/')

login_required(login_url='/login')
def Manage_user(request):
    user = User.objects.all()
    return render(request,"manage.html",{"i" : 1,"users" : user})


@login_required(login_url='/login')
def Jadikan_admin(request,id):
    user = get_object_or_404(User,id=id)
    user.is_staff = True
    user.save()
    return redirect('/manage/')