from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import OTP
from django.contrib.auth import login
from data_laundry.models import Barang
from django.contrib.auth.models import User

from django.utils import timezone

def otp_verify(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        user_id = request.session.get('temp_user_id')

        if not user_id:
            return redirect('/login/')

        otp_obj = OTP.objects.get(user_id=user_id)

        # === Cek apakah OTP kadaluarsa ===
        if otp_obj.expires_at and timezone.now() > otp_obj.expires_at:
            messages.error(request, "OTP sudah kadaluarsa, minta OTP baru.")
            return redirect('/isi/otp/')

        # === Cek OTP sesuai atau tidak ===
        if otp_input == otp_obj.code:
            user = otp_obj.user
            request.session.set_expiry(300)
            login(request, user)

            me = request.user
            request.session.pop('temp_user_id', None)

            if me.is_superuser:
                return redirect('/daftar_laundry_super/')
            elif me.is_staff:
                return redirect('/daftar_laundry_admin/')
            else:
                return redirect('/daftar_laundry_user/')

        messages.error(request, "OTP salah")
        return redirect('/isi/otp/')

    return render(request, 'otp_verify.html')
