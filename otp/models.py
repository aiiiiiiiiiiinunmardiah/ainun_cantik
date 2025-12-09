from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
import random

class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def generate(self):
        self.code = str(random.randint(100000, 999999))
        self.created_at = timezone.now()
        self.expires_at = timezone.now() + timedelta(minutes=5)  # OTP berlaku 5 menit
        self.save()
