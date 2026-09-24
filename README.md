# KEUVIA

**KEUVIA (Kelola Uang, Evaluasi, Visualisasi, dan Anggaran)** adalah aplikasi manajemen keuangan pribadi berbasis web yang dibuat untuk membantu pengguna mencatat, mengelola, dan memantau kondisi keuangan secara lebih terstruktur.

## Fitur

- Login dan autentikasi pengguna
- Registrasi akun
- Profil pengguna
- Ganti password
- Pencatatan pemasukan
- Pencatatan pengeluaran
- Manajemen kategori transaksi
- Edit transaksi
- Hapus transaksi
- Target tabungan
- Dashboard keuangan
- Grafik pemasukan dan pengeluaran
- Grafik pengeluaran berdasarkan kategori
- Filter laporan berdasarkan tanggal, kategori, dan tipe transaksi
- Pagination laporan
- Export laporan ke Excel
- Export laporan ke PDF
- Pemisahan data antar pengguna

## Teknologi

- **Python**
- **Flask**
- **PostgreSQL (Neon)**
- **HTML5**
- **CSS3**
- **JavaScript**
- **Chart.js**
- **Pandas**
- **OpenPyXL**
- **ReportLab**

## Struktur Project

```text
keuvia/
│
├── app.py
├── requirements.txt
├── .gitignore
├── .env
│
├── static/
│   ├── css/
│   └── js/
│
└── templates/
```

## Keamanan

KEUVIA menggunakan beberapa mekanisme keamanan dasar, antara lain:

- Password disimpan menggunakan password hashing.
- Sistem autentikasi menggunakan session.
- Data transaksi dibatasi berdasarkan pengguna yang sedang login.
- Data pengguna dipisahkan menggunakan user_id.
- Connection string database dan konfigurasi sensitif disimpan melalui environment variable.
- File konfigurasi sensitif tidak disimpan di repository publik.

## Dashboard

Dashboard menyediakan ringkasan kondisi keuangan pengguna, termasuk:

- Total pemasukan
- Total pengeluaran
- Saldo saat ini
- Jumlah transaksi
- Target tabungan
- Grafik pemasukan dan pengeluaran
- Visualisasi data keuangan berdasarkan periode

## Target Tabungan

Pengguna dapat membuat target tabungan dengan menentukan:

- Nama target
- Nominal target
- Jumlah yang telah terkumpul
- Tanggal target

## Laporan

Halaman laporan menyediakan fitur filter berdasarkan:

- Tanggal awal
- Tanggal akhir
- Kategori
- Jenis transaksi
  Hasil laporan dapat diekspor ke:
- Excel
- PDF

## Menjalankan Secara Lokal

Ikuti langkah berikut untuk menjalankan KEUVIA di komputer Anda.

### 1. Clone Repository

```bash
git clone https://github.com/iqbalprakoso/fintrack.git
```

### 2. Masuk ke Folder Project

```bash
cd fintrack
```

### 3. Buat Virtual Environment

```bash
python -m venv venv
```

Aktifkan virtual environment:
Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Konfigurasi Environment

Buat file .env dan masukkan konfigurasi database serta secret key aplikasi.
Contoh:

```text
DATABASE_URL=your_database_connection_string
SECRET_KEY=your_secret_key
```

Jangan membagikan isi .env atau connection string database ke publik.

### 6. Jalankan Aplikasi

```bash
python app.py
```

### 7. Buka Aplikasi

```bash
http://127.0.0.1:5000
```

Author
Iqbal Prakoso
KEUVIA dibuat sebagai project web application untuk pembelajaran, penggunaan pribadi, dan portfolio development.
