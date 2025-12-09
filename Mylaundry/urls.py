from django.contrib import admin
from django.urls import path,include
from . import view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',view.My_login),
    path('register/',view.register_user),
    path('adrg/',view.register_admin),
    path('sprg/',view.register_super_admin),
    path('daftar_laundry_user/',view.daftar_laundry_user),
    path('daftar_laundry_admin/',view.daftar_laundry_admin),
    path('daftar_laundry_super/',view.daftar_laundry_super),
    path('tambah/',include("data_laundry.urls")),
    path('isi/',include("otp.urls")),
    path('logout/',view.Mylog_out),
    path('kirim/',view.test_email),
    path('edit/<int:id>/', view.edit_barang),
    path('hapus/<int:id>/', view.hapus_barang),
    path('manage/',view.Manage_user),
    path('jadikan_admin/<int:id>/',view.Jadikan_admin)
]