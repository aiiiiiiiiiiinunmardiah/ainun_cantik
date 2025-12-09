from django.urls import path
from .views import otp_verify
urlpatterns = [
    path('otp/',otp_verify),
]