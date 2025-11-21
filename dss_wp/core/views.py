from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import stakeholder, alternatif, kriteria, NilaiEvaluasi
from core.utils import hitung_wp, hitung_borda

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

@login_required
def dashboard_view(request):
    stakeholder_profile = getattr(request.user, 'stakeholder_profile', None)
    return render(request, 'dashboard.html', {'stakeholder': stakeholder_profile})

def logout_view(request):
    logout(request)
    return redirect('login')

def input_nilai_view(request, stakeholder_id):
    # Ambil stakeholder berdasarkan ID
    stake = stakeholder.objects.get(id=stakeholder_id)
    all_alt = alternatif.objects.all()
    all_krit = kriteria.objects.all()

    if request.method == 'POST':
        # (Opsional) hapus data lama sebelum simpan baru
        NilaiEvaluasi.objects.filter(stakeholder=stake).delete()

        # Simpan nilai evaluasi baru
        for alt in all_alt:
            for k in all_krit:
                nilai_key = f'nilai_{alt.id}_{k.id}'
                nilai_value = request.POST.get(nilai_key)
                if nilai_value:
                    NilaiEvaluasi.objects.create(
                        stakeholder=stake,
                        alternatif=alt,
                        kriteria=k,
                        nilai=float(nilai_value)
                    )

        messages.success(request, 'Nilai evaluasi berhasil disimpan.')
        return redirect('hasil-wp', stakeholder_id=stake.id)

    context = {
        'stakeholder': stake,
        'alternatif_list': all_alt,
        'kriteria_list': all_krit
    }
    return render(request, 'input-nilai.html', context)

def hasil_wp_view(request, stakeholder_id):

    # ambil stakeholder berdasarkan ID
    stake = get_object_or_404(stakeholder, id=stakeholder_id)
    
    try:
        hasil_wp = hitung_wp(stake)
    except Exception as e:
        messages.error(request, f'Error menghitung WP: {str(e)}')
        hasil = []
        return redirect('input-nilai', stakeholder_id=stake.id)

    context = {
        'stake': stake,
        'hasil_wp': hasil_wp
    }
    return render(request, 'hasil-wp.html', context)

def hasil_borda_view(request):
    data = hitung_borda()
    return render(request, 'hasil-borda.html', data)