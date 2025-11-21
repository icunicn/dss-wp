# DSS WP - Sistem Pendukung Keputusan (Weighted Product & Borda)

Sistem Pendukung Keputusan berbasis Django yang mengimplementasikan metode Weighted Product (WP) dan Borda untuk pengambilan keputusan multi-kriteria.

## Fitur

- **Metode Weighted Product (WP)**: Menghitung skor weighted product untuk alternatif berdasarkan evaluasi stakeholder
- **Metode Borda**: Mengagregasi hasil WP dari multiple stakeholder menggunakan sistem ranking Borda
- **Dukungan Multi-Stakeholder**: Berbagai stakeholder dapat memasukkan nilai evaluasi secara independen
- **Autentikasi Pengguna**: Sistem login aman untuk stakeholder
- **Template Responsif**: Template HTML Django untuk visualisasi hasil

## Prasyarat

- Python 3.8+
- Django 5.2+
- NumPy
- pip (Python package manager)

## Instalasi

### 1. Clone atau Download Proyek

```bash
cd e:\Coding\Python\dss_wp
```

### 2. Buat Virtual Environment

```bash
python -m venv venv
```

### 3. Aktifkan Virtual Environment

**Pada Windows:**

```bash
venv\Scripts\activate
```

**Pada macOS/Linux:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

Jika file `requirements.txt` tidak ada, install secara manual:

```bash
pip install Django==5.2.8
pip install numpy
```

### 5. Jalankan Migrasi Database

```bash
python manage.py migrate
```

### 6. Buat Superuser (Akun Admin)

```bash
python manage.py createsuperuser
```

Ikuti petunjuk untuk membuat akun admin.

### 7. Jalankan Development Server

```bash
python manage.py runserver
```

Aplikasi akan tersedia di: `http://127.0.0.1:8000/`

## Cara Penggunaan

### 1. Login

- Navigasi ke `http://127.0.0.1:8000/` dan login dengan kredensial Anda

### 2. Input Nilai Evaluasi

- Pergi ke halaman "Input Nilai"
- Masukkan skor evaluasi untuk setiap alternatif terhadap setiap kriteria
- Klik "Simpan"

### 3. Lihat Hasil WP

- Setelah menyimpan, Anda akan dialihkan ke halaman hasil WP
- Halaman ini menampilkan skor Weighted Product yang dihitung untuk stakeholder tersebut

### 4. Lihat Hasil Borda

- Navigasi ke "Hasil Borda" untuk melihat hasil agregat dari semua stakeholder
- Metode Borda menggabungkan ranking dari multiple stakeholder

## Struktur Proyek

```
dss_wp/
├── dss_wp/                 # Konfigurasi proyek utama
│   ├── settings.py        # Pengaturan Django
│   ├── urls.py            # Konfigurasi URL utama
│   └── wsgi.py
├── core/                  # Aplikasi utama
│   ├── models.py          # Model database
│   ├── views.py           # Fungsi view
│   ├── urls.py            # Konfigurasi URL aplikasi
│   ├── utils.py           # Logika kalkulasi WP dan Borda
│   ├── templatetags/
│   │   └── dict_extras.py # Filter template kustom
│   └── templates/         # Template HTML
│       ├── login.html
│       ├── dashboard.html
│       ├── input-nilai.html
│       ├── hasil-wp.html
│       └── hasil-borda.html
├── manage.py              # Script manajemen Django
├── db.sqlite3             # Database (dibuat setelah migrasi)
└── README.md              # File ini
```

## Komponen Utama

### Model Database

- **stakeholder**: Pengguna yang memberikan evaluasi
- **alternatif**: Alternatif keputusan yang dievaluasi
- **kriteria**: Kriteria evaluasi
- **NilaiEvaluasi**: Skor evaluasi dari stakeholder
- **HasilWP**: Hasil kalkulasi WP
- **HasilBorda**: Hasil kalkulasi Borda

### Fungsi Utama

#### `hitung_wp(stakeholder_data)`

Menghitung skor Weighted Product untuk stakeholder tertentu:

- Normalisasi bobot kriteria
- Aplikasi transformasi benefit/cost
- Komputasi formula WP dengan kalkulasi pangkat

#### `hitung_borda()`

Mengagregasi hasil WP menggunakan metode Borda:

- Generate bobot Borda berdasarkan jumlah alternatif
- Ranking alternatif per stakeholder
- Penjumlahan skor terbobot di semua stakeholder

### Filter Template Kustom

- `get_item`: Akses nilai dictionary di template
- `div`: Lakukan operasi pembagian di template

## Setup Database

Setelah menjalankan migrasi, populasi database dengan:

1. **Stakeholder** (melalui Django admin atau shell)
2. **Alternatif** (contoh: "Jurusan 1", "Jurusan 2", "Jurusan 3")
3. **Kriteria** (dengan bobot dan tipe: "benefit" atau "cost")

Contoh:

```python
from core.models import stakeholder, alternatif, kriteria

stakeholder.objects.create(nama="Budi Santoso", peran="Kaprodi")
alternatif.objects.create(nama="Jurusan 1")
kriteria.objects.create(nama="Akreditasi", bobot=0.3, tipe="benefit")
```

## Troubleshooting

### Error: `'dict_extras' is not a registered tag library`

- Pastikan file `templatetags/dict_extras.py` ada di aplikasi core
- Verifikasi bahwa `templatetags/__init__.py` ada (bisa kosong)

### Error: `VariableDoesNotExist`

- Periksa bahwa semua variabel context yang diperlukan dilewatkan dari views
- Verifikasi bahwa filter template kustom didefinisikan dengan benar

### Error Database

- Jalankan `python manage.py migrate` untuk menerapkan migrasi yang tertunda
- Periksa izin file database

## Tips Pengembangan

- Gunakan `python manage.py shell` untuk menguji model dan fungsi secara interaktif
- Periksa log Django untuk pesan error detail
- Gunakan statement `print()` di utils.py untuk debugging kalkulasi

## Lisensi

Proyek ini untuk tujuan pendidikan.

## Dukungan

Untuk pertanyaan atau masalah, lihat dokumentasi Django: https://docs.djangoproject.com/
