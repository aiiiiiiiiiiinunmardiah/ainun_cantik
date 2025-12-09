from django.urls import path
from . import views

urlpatterns = [
    path('laundry/',views.tambah_laundry)
]