from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class stakeholder(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stakeholder_profile')
    nama = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nama} ({self.role})"

class kriteria(models.Model):
    id = models.AutoField(primary_key=True)
    nama = models.TextField()
    tipe = models.CharField(max_length=10, choices=[('benefit', 'Benefit'), ('cost', 'Cost')])
    bobot = models.FloatField()

    def __str__(self):
        return f"{self.nama} ({self.tipe}) - Bobot: {self.bobot}"

class alternatif(models.Model):
    id = models.AutoField(primary_key=True)
    nama = models.TextField()

    def __str__(self):
        return self.nama
    
class NilaiEvaluasi(models.Model):
    id = models.AutoField(primary_key=True)
    stakeholder = models.ForeignKey(stakeholder, on_delete=models.CASCADE)
    alternatif = models.ForeignKey(alternatif, on_delete=models.CASCADE)
    kriteria = models.ForeignKey(kriteria, on_delete=models.CASCADE)
    nilai = models.FloatField()

    def __str__(self):
        return f"{self.stakeholder.nama} ->  {self.alternatif.nama} - [{self.kriteria.nama}: {self.nilai}]"

class HasilWP(models.Model):
    id = models.AutoField(primary_key=True)
    stakeholder = models.ForeignKey(stakeholder, on_delete=models.CASCADE)
    alternatif = models.ForeignKey(alternatif, on_delete=models.CASCADE)
    skor = models.FloatField()

    def __str__(self):
        return f"{self.alternatif.nama} (oleh {self.stakeholder.nama}) → Skor WP: {self.skor:.4f}"
    
class HasilBorda(models.Model):
    id = models.AutoField(primary_key=True)
    alternatif = models.ForeignKey(alternatif, on_delete=models.CASCADE)
    skor = models.FloatField()
    rangking = models.IntegerField()

    def __str__(self):
        return f"{self.alternatif.nama} → Skor Borda: {self.skor:.4f}, Peringkat: {self.rangking}"
    