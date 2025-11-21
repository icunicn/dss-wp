import numpy as np
from .models import kriteria, NilaiEvaluasi, HasilWP, alternatif, HasilBorda, stakeholder
from django.db.models import Count

def hitung_wp(stakeholder_data):
    """
    Menghitung Weighted Product (WP) untuk data stakeholder.
    """
    # Ambil semua kriteria dan alternatif
    kriteria_list = list(kriteria.objects.all())
    alternatif_list = list(alternatif.objects.all())
    bobot = [k.bobot for k in kriteria_list]

    # Normalisasi bobot
    total_bobot = sum(bobot)
    bobot_normalized = [b / total_bobot for b in bobot]

    # Hapus hasil lama stakeholder ini
    HasilWP.objects.filter(stakeholder=stakeholder_data).delete()

    # Hitung skor WP
    result = []
    for alt in alternatif_list:
        skor_wp = 1
        for idx, k in enumerate(kriteria_list):
            try:
                nilai_kriteria = NilaiEvaluasi.objects.get(
                    stakeholder=stakeholder_data,
                    alternatif=alt,
                    kriteria=k
                ).nilai
            except NilaiEvaluasi.DoesNotExist:
                nilai_kriteria = 0

            # Jika kriteria cost, nilai dibalik
            if k.tipe == 'cost':
                nilai_kriteria = 1 / nilai_kriteria if nilai_kriteria != 0 else 0

            print(f"{alt.nama} | {k.nama} ({k.tipe}): {nilai_kriteria} -> bobot: {bobot_normalized[idx]}")
            skor_wp *= np.power(nilai_kriteria, bobot_normalized[idx])

        result.append({'alternatif': alt, 'skor_wp': skor_wp})

    # Normalisasi hasil agar total = 1
    total = sum(item['skor_wp'] for item in result)
    for item in result:
        nilai_akhir = item['skor_wp'] / total if total != 0 else 0
        HasilWP.objects.create(
            stakeholder=stakeholder_data,
            alternatif=item['alternatif'],
            skor=nilai_akhir
        )

    # Kembalikan hasil urut dari skor tertinggi
    hasil_result = HasilWP.objects.filter(stakeholder=stakeholder_data).order_by('-skor')
    return hasil_result


def generate_borda_weights(jumlah_rangking):
    """
    Menghasilkan bobot Borda berdasarkan jumlah peringkat.
    """
    return {
        rank : (jumlah_rangking - rank + 1)
        for rank in range(1, jumlah_rangking + 1)
    }

def hitung_borda():

    HasilBorda.objects.all().delete()

    semua_alt = list(alternatif.objects.all())
    jumlah_alt = len(semua_alt)

    bobot_borda = generate_borda_weights(jumlah_alt)

    # ===== tabel bobot borda =====
    bobot_borda_tabel = [
        {"rank": r, "bobot": bobot_borda[r]}
        for r in range(1, jumlah_alt + 1)
    ]

    stakeholder_list = stakeholder.objects.annotate(
        wp_count=Count('hasilwp')
    ).filter(wp_count__gt=0)

    borda_total = {alt.id: 0 for alt in semua_alt}

    # untuk tampilan WP per stakeholder
    wp_per_stakeholder = []

    # untuk tampilan hasil borda per alternatif seperti Excel
    borda_row_detail = {
        alt.id: {
            "alternatif": alt.nama,
            "rank_scores": {r: 0 for r in range(1, jumlah_alt + 1)},
            "poin_borda": 0
        }
        for alt in semua_alt
    }

    # =============================
    # PROSES SETIAP STAKEHOLDER
    # =============================
    detail = []

    for s in stakeholder_list:

        hasil_wp_stake = list(
            HasilWP.objects.filter(stakeholder=s).order_by('-skor')
        )

        # simpan untuk tampilan di atas
        wp_per_stakeholder.append({
            "stakeholder": s.nama,
            "data": hasil_wp_stake
        })

        for rank, hasil in enumerate(hasil_wp_stake, start=1):
            poin = hasil.skor * bobot_borda[rank]
            borda_total[hasil.alternatif.id] += poin

            # update row detail tabel Borda
            borda_row_detail[hasil.alternatif.id]["rank_scores"][rank] += hasil.skor
            borda_row_detail[hasil.alternatif.id]["poin_borda"] += poin

            detail.append({
                'stakeholder': s.nama,
                'alternatif': hasil.alternatif.nama,
                'rank': rank,
                'poin': poin
            })

    # =============================
    # SIMPAN HASIL BORDA
    # =============================
    sorted_borda = sorted(borda_total.items(), key=lambda x: x[1], reverse=True)

    final_output = []
    rank_counter = 1

    for alt_id, total_skor in sorted_borda:
        alt = alternatif.objects.get(id=alt_id)

        HasilBorda.objects.create(
            alternatif=alt,
            skor=total_skor,
            rangking=rank_counter
        )

        final_output.append({
            'alternatif': alt,
            'skor': total_skor,
            'rangking': rank_counter
        })

        rank_counter += 1

    return {
        "final_output": final_output,
        "detail": detail,
        "stakeholder_list": stakeholder_list,
        "wp_per_stakeholder": wp_per_stakeholder,
        "bobot_borda_tabel": bobot_borda_tabel,
        "borda_row_detail": borda_row_detail,
        "borda_total_sum": sum(borda_total.values())
    }
