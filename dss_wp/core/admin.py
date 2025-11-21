from django.contrib import admin
from .models import stakeholder, kriteria, alternatif, NilaiEvaluasi, HasilWP, HasilBorda

# Register your models here.
@admin.register(stakeholder)
class StakeholderAdmin(admin.ModelAdmin):
    list_display = ('nama', 'email', 'role')
    search_fields = ('nama', 'email', 'role')
    list_filter = ('role',)


@admin.register(kriteria)
class KriteriaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'tipe', 'bobot')
    search_fields = ('nama',)
    list_filter = ('tipe',)

@admin.register(alternatif)
class AlternatifAdmin(admin.ModelAdmin):
    list_display = ('nama',)
    search_fields = ('nama',)

@admin.register(NilaiEvaluasi)
class NilaiEvaluasiAdmin(admin.ModelAdmin):
    list_display = ('stakeholder', 'alternatif', 'kriteria', 'nilai')
    search_fields = ('stakeholder__nama', 'alternatif__nama', 'kriteria__nama')
    list_filter = ('kriteria__tipe',)

@admin.register(HasilWP)
class HasilWPAdmin(admin.ModelAdmin):
    list_display = ('stakeholder', 'alternatif', 'skor')
    search_fields = ('stakeholder__nama', 'alternatif__nama')

@admin.register(HasilBorda)
class HasilBordaAdmin(admin.ModelAdmin):
    list_display = ('alternatif', 'skor', 'rangking')
    search_fields = ('alternatif__nama',)
    ordering = ('rangking',)