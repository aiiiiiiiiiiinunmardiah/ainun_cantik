from django.db import models

class Barang(models.Model):
    nama = models.CharField(max_length=100)
    jenis = models.CharField(max_length=50)
    berat = models.FloatField()          # contoh: 1.5 kg
    harga = models.IntegerField()        # contoh: 15000
    status = models.CharField(
        max_length=20,
        choices=[
            ('proses', 'Proses'),
            ('selesai', 'Selesai'),
        ],
        default='proses'
    )

    def __str__(self):
        return self.nama
