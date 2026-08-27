# FINTRACK

**FINTRACK** adalah aplikasi manajemen keuangan pribadi berbasis web yang dibuat untuk membantu pengguna mencatat, mengelola, dan memantau kondisi keuangan secara lebih terstruktur.

## Fitur

-  Login dan autentikasi pengguna
-  Registrasi akun
-  Profil pengguna
-  Ganti password
-  Pencatatan pemasukan
-  Pencatatan pengeluaran
-  Manajemen kategori transaksi
-  Edit transaksi
-  Hapus transaksi
-  Target tabungan
-  Dashboard keuangan
-  Grafik pemasukan dan pengeluaran
-  Grafik pengeluaran berdasarkan kategori
-  Filter laporan berdasarkan tanggal, kategori, dan tipe transaksi
-  Pagination laporan
-  Export laporan ke Excel
-  Export laporan ke PDF
-  Pemisahan data antar pengguna

## Teknologi

- **Python**
- **Flask**
- **SQLite**
- **HTML5**
- **CSS3**
- **JavaScript**
- **Chart.js**
- **Pandas**
- **OpenPyXL**
- **ReportLab**

## Struktur Project

```text
fintrack/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── static/
│   ├── css/
│   └── js/
│
└── templates/
```


## Keamanan

FINTRACK menggunakan beberapa mekanisme keamanan dasar, antara lain:

Password disimpan menggunakan password hashing.
Sistem autentikasi menggunakan session.
Data transaksi dibatasi berdasarkan pengguna yang sedang login.
Data pengguna tidak dicampur dengan pengguna lainnya.
Database lokal dan file konfigurasi sensitif tidak disimpan di repository publik.

## Dashboard

Dashboard menyediakan ringkasan kondisi keuangan pengguna, termasuk pemasukan, pengeluaran, saldo, jumlah transaksi, serta visualisasi data keuangan berdasarkan periode dan kategori.

## Target Tabungan

Pengguna dapat membuat target tabungan dengan menentukan nama target, nominal target, jumlah yang telah terkumpul, dan tanggal target.

## Laporan

Halaman laporan menyediakan fitur filter berdasarkan:
Tanggal awal
Tanggal akhir
Kategori
Jenis transaksi
Hasil laporan dapat diekspor ke format Excel dan PDF.

## Menjalankan Secara Lokal

Ikuti langkah berikut untuk menjalankan FINTRACK di komputer Anda.

### 1. Clone Repository

```bash
git clone https://github.com/iqbalprakoso/fintrack.git
```

### 2. Masuk ke Folder Project

```bash
cd fintrack
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi

```bash
python app.py
```

### 5. Buka FINTRACK

Setelah aplikasi berhasil dijalankan, buka browser dan akses:

```text
http://127.0.0.1:5000
```

👨‍💻 Author
Iqbal Prakoso

FINTRACK dibuat sebagai project web application untuk pembelajaran, penggunaan pribadi, dan portfolio development.

⭐ Jika project ini bermanfaat, silakan beri star pada repository.
