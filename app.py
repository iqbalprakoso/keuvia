# ==========================================================
# CATATAN KEUANGAN DASHBOARD
# APP.PY
# ----------------------------------------------------------
# Author  : Iqbal Prakoso
# Framework : Flask
# Database  : SQLite
# ==========================================================


# ==========================================================
# IMPORT LIBRARY
# ==========================================================

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    send_file,
    flash,
    url_for,
    session
)


import os
import pandas as pd

import psycopg
from psycopg.rows import dict_row

from dotenv import load_dotenv

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import (
    datetime,
    date
)

# ==========================================================
# MEMBUAT APLIKASI FLASK
# ==========================================================

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY",
    "dev-secret-key"
)

# ==========================================================
# PROTEKSI LOGIN
# ==========================================================

@app.before_request
def cek_login():

    # Halaman yang boleh diakses tanpa login
    halaman_public = [
        "login",
        "register",
        "logout",
        "static"
    ]

    # Kalau endpoint termasuk halaman public
    if request.endpoint in halaman_public:
        return

    # Kalau belum login
    if "user_id" not in session:
        return redirect("/login")


# ==========================================================
# REGISTER / DAFTAR AKUN
# ==========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    # Kalau sudah login, tidak perlu daftar lagi
    if session.get("user_id"):
        return redirect("/")

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"]
        konfirmasi = request.form["konfirmasi"]


        # ==================================================
        # VALIDASI USERNAME
        # ==================================================

        if not username:

            flash(
                "Username wajib diisi.",
                "error"
            )

            return redirect("/register")


        if len(username) < 3:

            flash(
                "Username minimal 3 karakter.",
                "error"
            )

            return redirect("/register")


        # ==================================================
        # VALIDASI PASSWORD
        # ==================================================

        if len(password) < 6:

            flash(
                "Password minimal 6 karakter.",
                "error"
            )

            return redirect("/register")


        # ==================================================
        # KONFIRMASI PASSWORD
        # ==================================================

        if password != konfirmasi:

            flash(
                "Konfirmasi password tidak sama.",
                "error"
            )

            return redirect("/register")


        # ==================================================
        # DATABASE
        # ==================================================

        conn = get_db()


        # Cek username sudah digunakan atau belum
        user = conn.execute("""
            SELECT id
            FROM users
            WHERE username = %s
        """, (username,)).fetchone()


        if user:

            conn.close()

            flash(
                "Username sudah digunakan. Silakan pilih username lain.",
                "error"
            )

            return redirect("/register")


        # ==================================================
        # HASH PASSWORD
        # ==================================================

        password_hash = generate_password_hash(
            password
        )


        # ==================================================
        # SIMPAN USER BARU
        # ==================================================

        conn.execute("""
            INSERT INTO users(
                username,
                password
            )
            VALUES(%s, %s)
        """, (
            username,
            password_hash
        ))


        conn.commit()
        conn.close()


        # ==================================================
        # BERHASIL
        # ==================================================

        flash(
            "Akun berhasil dibuat. Silakan login.",
            "success"
        )

        return redirect("/login")


    return render_template(
        "register.html"
    )


# ==========================================================
# LOGOUT
# ==========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

# ==========================================================
# NAMA DATABASE
# ==========================================================

DATABASE = "database.db"

# ==========================================================
# DICTIONARY NAMA BULAN INDONESIA
# Digunakan oleh filter tanggal_indo
# ==========================================================

BULAN = {

    "01": "Januari",
    "02": "Februari",
    "03": "Maret",
    "04": "April",
    "05": "Mei",
    "06": "Juni",
    "07": "Juli",
    "08": "Agustus",
    "09": "September",
    "10": "Oktober",
    "11": "November",
    "12": "Desember"

}


@app.context_processor
def inject_today():
    return {
        "today": date.today()
    }

# ==========================================================
# FILTER JINJA
# FORMAT TANGGAL INDONESIA
# ==========================================================

@app.template_filter("tanggal_indo")
def tanggal_indo(tanggal):

    if not tanggal:
        return "-"

    try:
        if isinstance(tanggal, str):
            tanggal = datetime.strptime(
                tanggal,
                "%Y-%m-%d"
            )

        return f"{tanggal.day:02d} {BULAN[tanggal.strftime('%m')]} {tanggal.year}"

    except:
        return tanggal

# ==========================================================
# FILTER JINJA
# FORMAT ANGKA MENJADI RUPIAH
# ==========================================================

@app.template_filter("rupiah")
def rupiah(angka):

    if angka is None:
        angka = 0

    return f"Rp {angka:,.0f}".replace(",", ".")

# ==========================================================
# KONEKSI DATABASE
# PostgreSQL Neon
# ==========================================================

def get_db():

    conn = psycopg.connect(
        os.getenv("DATABASE_URL"),
        row_factory=dict_row
    )

    return conn

# ==========================================================
# MENGAMBIL WARNA UNTUK KATEGORI BARU
# ==========================================================

def get_next_category_color(conn):

    warna_digunakan = conn.execute("""
        SELECT warna
        FROM kategori
        WHERE warna IS NOT NULL
    """).fetchall()

    warna_digunakan = {
        row["warna"]
        for row in warna_digunakan
    }

    # Cari warna pertama yang belum digunakan
    for warna in WARNA_KATEGORI:

        if warna not in warna_digunakan:

            return warna

    # Kalau semua warna sudah digunakan,
    # gunakan warna berdasarkan jumlah kategori
    jumlah = conn.execute("""
        SELECT COUNT(*) AS jumlah
        FROM kategori
    """).fetchone()["jumlah"]

    return WARNA_KATEGORI[
        jumlah % len(WARNA_KATEGORI)
    ]

# ==========================================================
# WARNA KATEGORI
# ==========================================================

WARNA_KATEGORI = [
    "#36A2EB",  # Biru
    "#FF6384",  # Pink
    "#FF9F40",  # Oranye
    "#8E44AD",  # Ungu
    "#FFCD56",  # Kuning
    "#4BC0C0",  # Cyan
    "#16A085",  # Hijau
    "#3498DB",  # Biru muda
    "#E67E22",  # Oranye tua
    "#9C27B0",  # Ungu
]

# ==========================================================
# MEMBUAT TABEL DATABASE
# PostgreSQL Neon
# ==========================================================

def init_db():

    conn = get_db()

    # ======================================================
    # TABEL USERS
    # ======================================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    # ======================================================
    # TABEL TRANSAKSI
    # ======================================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS transaksi(
            id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
            tanggal TEXT NOT NULL,
            keterangan TEXT NOT NULL,
            kategori TEXT NOT NULL,
            tipe TEXT NOT NULL,
            nominal BIGINT NOT NULL,
            user_id BIGINT
        )
    """)

    # ======================================================
    # TABEL TARGET TABUNGAN
    # ======================================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS target_tabungan(
            id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
            nama_target TEXT NOT NULL,
            nominal_target BIGINT NOT NULL,
            tanggal_target TEXT,
            terkumpul BIGINT DEFAULT 0,
            user_id BIGINT
        )
    """)

    # ======================================================
    # TABEL KATEGORI
    # ======================================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS kategori(
            id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
            nama TEXT NOT NULL,
            tipe TEXT NOT NULL,
            user_id BIGINT,
            warna TEXT
        )
    """)

    # ======================================================
    # TAMBAHKAN KOLOM JIKA DATABASE SUDAH PERNAH DIBUAT
    # ======================================================

    conn.execute("""
        ALTER TABLE transaksi
        ADD COLUMN IF NOT EXISTS user_id BIGINT
    """)

    conn.execute("""
        ALTER TABLE target_tabungan
        ADD COLUMN IF NOT EXISTS terkumpul BIGINT DEFAULT 0
    """)

    conn.execute("""
        ALTER TABLE target_tabungan
        ADD COLUMN IF NOT EXISTS user_id BIGINT
    """)

    conn.execute("""
        ALTER TABLE kategori
        ADD COLUMN IF NOT EXISTS user_id BIGINT
    """)

    conn.execute("""
        ALTER TABLE kategori
        ADD COLUMN IF NOT EXISTS warna TEXT
    """)

    # ======================================================
    # AKUN ADMIN DEFAULT
    # ======================================================

    admin = conn.execute("""
        SELECT id
        FROM users
        WHERE username = %s
    """, ("admin",)).fetchone()

    if not admin:

        password_hash = generate_password_hash("admin123")

        conn.execute("""
            INSERT INTO users(
                username,
                password
            )
            VALUES(%s, %s)
        """, (
            "admin",
            password_hash
        ))

    # ======================================================
    # AMBIL ID ADMIN
    # ======================================================

    admin = conn.execute("""
        SELECT id
        FROM users
        WHERE username = %s
    """, ("admin",)).fetchone()

    admin_id = admin["id"]

    # ======================================================
    # DATA LAMA YANG BELUM MEMILIKI USER
    # MENJADI MILIK ADMIN
    # ======================================================

    conn.execute("""
        UPDATE transaksi
        SET user_id = %s
        WHERE user_id IS NULL
    """, (admin_id,))

    conn.execute("""
        UPDATE target_tabungan
        SET user_id = %s
        WHERE user_id IS NULL
    """, (admin_id,))

    conn.execute("""
        UPDATE kategori
        SET user_id = %s
        WHERE user_id IS NULL
    """, (admin_id,))

    # ======================================================
    # MEMBERIKAN WARNA PADA KATEGORI
    # YANG BELUM MEMILIKI WARNA
    # ======================================================

    kategori_tanpa_warna = conn.execute("""
        SELECT id
        FROM kategori
        WHERE warna IS NULL
        ORDER BY id
    """).fetchall()

    for item in kategori_tanpa_warna:

        warna = get_next_category_color(conn)

        conn.execute("""
            UPDATE kategori
            SET warna = %s
            WHERE id = %s
        """, (
            warna,
            item["id"]
        ))

    # ======================================================
    # SIMPAN DATABASE
    # ======================================================

    conn.commit()

    conn.close()

# ==========================================================
# HELPER FUNCTION
# Seluruh fungsi pengambilan data dashboard
# ==========================================================


# ==========================================================
# RINGKASAN KEUANGAN
# Hanya menghitung transaksi milik user yang sedang login
# ==========================================================

def get_summary(conn):

    result = conn.execute("""
        SELECT

            COALESCE(
                SUM(
                    CASE
                        WHEN tipe = 'Pemasukan'
                        THEN nominal
                        ELSE 0
                    END
                ),
                0
            ) AS pemasukan,

            COALESCE(
                SUM(
                    CASE
                        WHEN tipe = 'Pengeluaran'
                        THEN nominal
                        ELSE 0
                    END
                ),
                0
            ) AS pengeluaran

        FROM transaksi

        WHERE user_id = %s
    """, (
        session["user_id"],
    )).fetchone()


    pemasukan = result["pemasukan"]

    pengeluaran = result["pengeluaran"]

    saldo = pemasukan - pengeluaran


    return {

        "pemasukan": pemasukan,

        "pengeluaran": pengeluaran,

        "saldo": saldo

    }

# ==========================================================
# TARGET TABUNGAN TERAKHIR
# Hanya mengambil target milik user yang sedang login
# ==========================================================

def get_target(conn):

    target = conn.execute("""
        SELECT *
        FROM target_tabungan

        WHERE user_id = %s

        ORDER BY id DESC

        LIMIT 1
    """, (
        session["user_id"],
    )).fetchone()

    return target

# ==========================================================
# AMBIL SEMUA TARGET TABUNGAN
# Hanya target milik user yang sedang login
# ==========================================================

def get_all_targets(conn):

    targets = conn.execute("""

        SELECT *
        FROM target_tabungan

        WHERE user_id = %s

        ORDER BY id DESC

    """, (
        session["user_id"],
    )).fetchall()

    return targets

# ==========================================================
# PROGRESS TARGET TABUNGAN
# ==========================================================

def get_target_progress(target, saldo):

    if not target:

        return {
            "progress": 0,
            "sisa": 0
        }

    nominal_target = target["nominal_target"]

    if nominal_target <= 0:

        return {
            "progress": 0,
            "sisa": 0
        }

    progress = min(

        round(
            (saldo / nominal_target) * 100,
            1
        ),
          100
    )

    sisa = max(
        nominal_target - saldo,
        0
    )

    return {

        "progress": progress,
        "sisa": sisa
    }

# ==========================================================
# TRANSAKSI TERBARU
# Hanya transaksi milik user yang sedang login
# ==========================================================

def get_recent_transactions(conn):

    data = conn.execute("""
        SELECT *
        FROM transaksi

        WHERE user_id = %s

        ORDER BY tanggal DESC, id DESC

        LIMIT 5
    """, (
        session["user_id"],
    )).fetchall()

    return data

# ==========================================================
# GRAFIK BULANAN
# Hanya data milik user yang sedang login
# ==========================================================

def get_monthly_chart(conn):

    result = conn.execute("""

        SELECT
            TO_CHAR(tanggal::date, 'YYYY-MM') AS bulan,

            COALESCE(
                SUM(
                    CASE
                        WHEN tipe = 'Pemasukan'
                        THEN nominal
                        ELSE 0
                    END
                ),
                0
            ) AS pemasukan,

            COALESCE(
                SUM(
                    CASE
                        WHEN tipe = 'Pengeluaran'
                        THEN nominal
                        ELSE 0
                    END
                ),
                0
            ) AS pengeluaran

        FROM transaksi

        WHERE user_id = %s

        GROUP BY TO_CHAR(tanggal::date, 'YYYY-MM')

        ORDER BY bulan

    """, (
        session["user_id"],
    )).fetchall()


    bulan_chart = []

    pemasukan_chart = []

    pengeluaran_chart = []


    for row in result:

        bulan_chart.append(
            row["bulan"]
        )

        pemasukan_chart.append(
            row["pemasukan"]
        )

        pengeluaran_chart.append(
            row["pengeluaran"]
        )


    return {

        "bulan": bulan_chart,

        "pemasukan": pemasukan_chart,

        "pengeluaran": pengeluaran_chart

    }


# ==========================================================
# DONUT CHART
# Pengeluaran Berdasarkan Kategori
# Hanya data milik user yang sedang login
# ==========================================================

def get_category_chart(conn):

    result = conn.execute("""

        SELECT
            kategori,
            SUM(nominal) AS total

        FROM transaksi

        WHERE tipe = 'Pengeluaran'
        AND user_id = %s

        GROUP BY kategori

        ORDER BY total DESC

    """, (
        session["user_id"],
    )).fetchall()


    kategori = []

    nominal = []


    for row in result:

        kategori.append(
            row["kategori"]
        )

        nominal.append(
            row["total"]
        )


    return {

        "kategori": kategori,

        "nominal": nominal

    }

# ==========================================================
# STATISTIK BULAN INI
# Hanya menghitung transaksi milik user yang sedang login
# ==========================================================

def get_dashboard_stats(conn):

    bulan = date.today().strftime("%Y-%m")


    # ======================================================
    # PEMASUKAN BULAN INI
    # ======================================================

    pemasukan_bulan_ini = conn.execute("""
        SELECT COALESCE(SUM(nominal), 0) AS total
        FROM transaksi
        WHERE tipe = 'Pemasukan'
        AND TO_CHAR(tanggal::date, 'YYYY-MM') = %s
        AND user_id = %s
    """, (
        bulan,
        session["user_id"]
    )).fetchone()["total"]


    # ======================================================
    # PENGELUARAN BULAN INI
    # ======================================================

    pengeluaran_bulan_ini = conn.execute("""
        SELECT COALESCE(SUM(nominal), 0) AS total
        FROM transaksi
        WHERE tipe = 'Pengeluaran'
        AND TO_CHAR(tanggal::date, 'YYYY-MM') = %s
        AND user_id = %s
    """, (
        bulan,
        session["user_id"]
    )).fetchone()["total"]


    # ======================================================
    # JUMLAH TRANSAKSI BULAN INI
    # ======================================================

    jumlah_transaksi = conn.execute("""
        SELECT COUNT(*) AS total
        FROM transaksi
        WHERE TO_CHAR(tanggal::date, 'YYYY-MM') = %s
        AND user_id = %s
    """, (
        bulan,
        session["user_id"]
    )).fetchone()["total"]


    return {

        "pemasukan_bulan_ini":
            pemasukan_bulan_ini,

        "pengeluaran_bulan_ini":
            pengeluaran_bulan_ini,

        "jumlah_transaksi":
            jumlah_transaksi

    }

# ==========================================================
# LOGIN
# ==========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    # Kalau sudah login
    if session.get("user_id"):

        return redirect("/")


    # Ketika form dikirim
    if request.method == "POST":

        username = request.form["username"].strip()

        password = request.form["password"]


        conn = get_db()

        user = conn.execute("""
            SELECT *
            FROM users
            WHERE username = %s
        """, (username,)).fetchone()

        conn.close()


        # Cek username dan password
        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = user["id"]

            session["username"] = user["username"]

            return redirect("/")


        flash(
            "Username atau password salah.",
            "error"
        )


    return render_template("login.html")


# ==========================================================
# ROUTE DASHBOARD
# Halaman utama aplikasi
# ==========================================================

@app.route("/")
def dashboard():

    # ---------------------------------------------
    # Membuka koneksi database
    # ---------------------------------------------

    conn = get_db()

    # ---------------------------------------------
    # Ringkasan Keuangan
    # ---------------------------------------------

    summary = get_summary(conn)

    # ---------------------------------------------
    # Target Tabungan
    # ---------------------------------------------

    target = get_target(conn)

    target_progress = get_target_progress(
        target,
        summary["saldo"]
    )

    # ---------------------------------------------
    # Grafik Dashboard
    # ---------------------------------------------

    monthly_chart = get_monthly_chart(conn)

    category_chart = get_category_chart(conn)

    # ---------------------------------------------
    # Statistik Bulan Ini
    # ---------------------------------------------

    stats = get_dashboard_stats(conn)

    # ---------------------------------------------
    # Transaksi Terbaru
    # ---------------------------------------------

    recent_transactions = get_recent_transactions(conn)

    # ---------------------------------------------
    # Tanggal Hari Ini
    # ---------------------------------------------

    today = date.today().strftime("%Y-%m-%d")

    # ---------------------------------------------
    # Tutup Koneksi
    # ---------------------------------------------

    conn.close()

    # ---------------------------------------------
    # Kirim Data ke dashboard.html
    # ---------------------------------------------

    return render_template(

        "dashboard.html",

        # ==========================
        # Tanggal
        # ==========================

        today=today,

        # ==========================
        # Ringkasan
        # ==========================

        pemasukan=summary["pemasukan"],
        pengeluaran=summary["pengeluaran"],
        saldo=summary["saldo"],

        # ==========================
        # Target
        # ==========================

        target=target,
        progress_target=target_progress["progress"],
        sisa_target=target_progress["sisa"],

        # ==========================
        # Statistik Bulan Ini
        # ==========================

        pemasukan_bulan_ini=stats["pemasukan_bulan_ini"],
        pengeluaran_bulan_ini=stats["pengeluaran_bulan_ini"],
        jumlah_transaksi_bulan_ini=stats["jumlah_transaksi"],

        # ==========================
        # Grafik Bar
        # ==========================

        bulan_chart=monthly_chart["bulan"],
        pemasukan_chart=monthly_chart["pemasukan"],
        pengeluaran_chart=monthly_chart["pengeluaran"],

        # ==========================
        # Grafik Donut
        # ==========================

        kategori=category_chart["kategori"],
        nominal=category_chart["nominal"],

        # ==========================
        # Transaksi Terbaru
        # ==========================

        data=recent_transactions

    )


# ==========================================================
# ROUTE TAMBAH TRANSAKSI
# Menyimpan transaksi milik user yang sedang login
# ==========================================================

@app.route("/tambah", methods=["POST"])
def tambah():

    conn = get_db()

    conn.execute("""
        INSERT INTO transaksi(
            tanggal,
            keterangan,
            kategori,
            tipe,
            nominal,
            user_id
        )
        VALUES(
            %s, %s, %s, %s, %s, %s
        )
    """, (

        request.form["tanggal"],
        request.form["keterangan"],
        request.form["kategori"],
        request.form["tipe"],
        int(request.form["nominal"]),
        session["user_id"]

    ))

    conn.commit()
    conn.close()

    flash(
        "Transaksi berhasil ditambahkan.",
        "success"
    )

    return redirect("/transaksi")

# ==========================================================
# ROUTE EDIT TRANSAKSI
# Hanya mengambil transaksi milik user sendiri
# ==========================================================

@app.route("/edit/<int:id>")
def edit(id):

    conn = get_db()

    transaksi = conn.execute("""
        SELECT *
        FROM transaksi
        WHERE id = %s
        AND user_id = %s
    """, (
        id,
        session["user_id"]
    )).fetchone()

    conn.close()

    if not transaksi:

        flash(
            "Transaksi tidak ditemukan.",
            "error"
        )

        return redirect("/transaksi")

    return render_template(
        "edit.html",
        transaksi=transaksi
    )


# ==========================================================
# ROUTE UPDATE TRANSAKSI
# Hanya mengubah transaksi milik user sendiri
# ==========================================================

@app.route("/update/<int:id>", methods=["POST"])
def update(id):

    conn = get_db()

    conn.execute("""
        UPDATE transaksi
        SET
            tanggal = %s,
            keterangan = %s,
            kategori = %s,
            tipe = %s,
            nominal = %s
        WHERE id = %s
        AND user_id = %s
    """, (

        request.form["tanggal"],
        request.form["keterangan"],
        request.form["kategori"],
        request.form["tipe"],
        int(request.form["nominal"]),

        id,
        session["user_id"]

    ))

    conn.commit()
    conn.close()

    flash(
        "Transaksi berhasil diperbarui.",
        "success"
    )

    return redirect("/transaksi")

# ==========================================================
# KATEGORI
# Hanya menampilkan kategori milik user yang sedang login
# ==========================================================

@app.route("/kategori")
def kategori():

    conn = get_db()

    data_kategori = conn.execute("""
        SELECT *
        FROM kategori
        WHERE user_id = %s
        ORDER BY tipe, nama
    """, (
        session["user_id"],
    )).fetchall()

    conn.close()

    return render_template(
        "kategori.html",
        data_kategori=data_kategori
    )

# ==========================================================
# TAMBAH KATEGORI
# Kategori menjadi milik user yang sedang login
# ==========================================================

@app.route("/kategori/tambah", methods=["POST"])
def tambah_kategori():

    conn = get_db()

    nama = request.form["nama"].strip()
    tipe = request.form["tipe"]

    if nama:

        conn.execute("""
            INSERT INTO kategori(
                nama,
                tipe,
                user_id
            )
            VALUES(%s, %s, %s)
        """, (
            nama,
            tipe,
            session["user_id"]
        ))

        conn.commit()

        flash(
            f"Kategori '{nama}' berhasil ditambahkan.",
            "success"
        )

    else:

        flash(
            "Nama kategori tidak boleh kosong.",
            "error"
        )

    conn.close()

    return redirect("/kategori")

# ==========================================================
# EDIT KATEGORI
# Hanya boleh mengedit kategori milik user sendiri
# ==========================================================

@app.route("/kategori/edit/<int:id>", methods=["POST"])
def edit_kategori(id):

    nama = request.form["nama"].strip()
    tipe = request.form["tipe"]

    conn = get_db()

    # ======================================================
    # CARI KATEGORI MILIK USER
    # ======================================================

    kategori_lama = conn.execute("""
        SELECT nama, tipe
        FROM kategori
        WHERE id = %s
        AND user_id = %s
    """, (
        id,
        session["user_id"]
    )).fetchone()


    # ======================================================
    # KATEGORI TIDAK DITEMUKAN
    # ======================================================

    if not kategori_lama:

        conn.close()

        flash(
            "Kategori tidak ditemukan.",
            "error"
        )

        return redirect("/kategori")


    nama_lama = kategori_lama["nama"]
    tipe_lama = kategori_lama["tipe"]


    # ======================================================
    # CEK APAKAH KATEGORI DIGUNAKAN TRANSAKSI USER INI
    # ======================================================

    digunakan = conn.execute("""
        SELECT COUNT(*) AS total
        FROM transaksi
        WHERE kategori = %s
        AND user_id = %s
    """, (
        nama_lama,
        session["user_id"]
    )).fetchone()["total"]

    # ======================================================
    # JIKA SUDAH DIGUNAKAN
    # TIPE TIDAK BOLEH BERUBAH
    # ======================================================

    if digunakan > 0:

        tipe = tipe_lama


    # ======================================================
    # UPDATE KATEGORI
    # ======================================================

    conn.execute("""
        UPDATE kategori
        SET
            nama = %s,
            tipe = %s
        WHERE id = %s
        AND user_id = %s
    """, (
        nama,
        tipe,
        id,
        session["user_id"]
    ))


    # ======================================================
    # SINKRONKAN NAMA KATEGORI PADA TRANSAKSI
    # MILIK USER YANG SAMA SAJA
    # ======================================================

    conn.execute("""
        UPDATE transaksi
        SET kategori = %s
        WHERE kategori = %s
        AND user_id = %s
    """, (
        nama,
        nama_lama,
        session["user_id"]
    ))


    # ======================================================
    # SIMPAN
    # ======================================================

    conn.commit()
    conn.close()

    flash(
        f"Kategori '{nama}' berhasil diperbarui.",
        "success"
    )

    return redirect("/kategori")

# ==========================================================
# HAPUS KATEGORI
# Hanya boleh menghapus kategori milik user sendiri
# ==========================================================

@app.route("/kategori/hapus/<int:id>", methods=["POST"])
def hapus_kategori(id):

    conn = get_db()


    # ======================================================
    # CARI KATEGORI MILIK USER
    # ======================================================

    kategori = conn.execute("""
        SELECT nama
        FROM kategori
        WHERE id = %s
        AND user_id = %s
    """, (
        id,
        session["user_id"]
    )).fetchone()


    # ======================================================
    # KATEGORI TIDAK DITEMUKAN
    # ======================================================

    if not kategori:

        conn.close()

        flash(
            "Kategori tidak ditemukan.",
            "error"
        )

        return redirect("/kategori")


    nama_kategori = kategori["nama"]


    # ======================================================
    # CEK APAKAH KATEGORI MASIH DIGUNAKAN
    # OLEH TRANSAKSI USER INI
    # ======================================================

    digunakan = conn.execute("""
        SELECT COUNT(*) AS total
        FROM transaksi
        WHERE kategori = %s
        AND user_id = %s
    """, (
        nama_kategori,
        session["user_id"]
    )).fetchone()["total"]


    # ======================================================
    # JIKA MASIH DIGUNAKAN
    # ======================================================

    if digunakan > 0:

        conn.close()

        flash(
            f"Kategori '{nama_kategori}' tidak dapat dihapus "
            f"karena masih digunakan oleh {digunakan} transaksi.",
            "error"
        )

        return redirect("/kategori")


    # ======================================================
    # HAPUS KATEGORI
    # ======================================================

    conn.execute("""
        DELETE FROM kategori
        WHERE id = %s
        AND user_id = %s
    """, (
        id,
        session["user_id"]
    ))


    conn.commit()
    conn.close()


    flash(
        f"Kategori '{nama_kategori}' berhasil dihapus.",
        "success"
    )

    return redirect("/kategori")

# ==========================================================
# PENGATURAN
# ==========================================================

@app.route("/pengaturan")
def pengaturan():

    return render_template(
        "pengaturan.html",
        today=date.today().strftime("%Y-%m-%d")
    )


# ==========================================================
# ROUTE EXPORT EXCEL
# Mengekspor seluruh transaksi ke file Excel
# ==========================================================

@app.route("/export")
def export_excel():

    conn = get_db()
    data = conn.execute("""
        SELECT
            tanggal,
            keterangan,
            kategori,
            tipe,
            nominal
        FROM transaksi
        WHERE user_id = %s
        ORDER BY tanggal DESC
    """, (
        session["user_id"],
    )).fetchall()

    conn.close()
    df = pd.DataFrame(
        data,
        columns=[
            "Tanggal",
            "Keterangan",
            "Kategori",
            "Tipe",
            "Nominal"
        ]

    )

    file_name = "catatan_keuangan.xlsx"
    with pd.ExcelWriter(
        file_name,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            sheet_name="Transaksi",
            index=False
        )

        ws = writer.sheets["Transaksi"]

        ws.column_dimensions["A"].width = 15
        ws.column_dimensions["B"].width = 35
        ws.column_dimensions["C"].width = 20
        ws.column_dimensions["D"].width = 15
        ws.column_dimensions["E"].width = 20

    return send_file(

        file_name,
        as_attachment=True

    )

# ==========================================================
# ROUTE TARGET TABUNGAN
# Hanya menampilkan target milik user yang sedang login
# ==========================================================

@app.route("/target", methods=["GET", "POST"])
def target():

    conn = get_db()

    # ======================================================
    # TAMBAH TARGET
    # ======================================================

    if request.method == "POST":

        conn.execute("""
            INSERT INTO target_tabungan(
                nama_target,
                nominal_target,
                terkumpul,
                tanggal_target,
                user_id
            )
            VALUES(%s, %s, %s, %s, %s)
        """, (

            request.form["nama_target"],
            int(request.form["nominal_target"]),
            int(request.form.get("terkumpul") or 0),
            request.form["tanggal_target"],
            session["user_id"]

        ))

        conn.commit()

        conn.close()

        flash(
            "Target berhasil ditambahkan.",
            "success"
        )

        return redirect("/target")


    # ======================================================
    # AMBIL TARGET MILIK USER
    # ======================================================

    targets = conn.execute("""
        SELECT *
        FROM target_tabungan
        WHERE user_id = %s
        ORDER BY id DESC
    """, (
        session["user_id"],
    )).fetchall()


    # ======================================================
    # HITUNG PROGRESS
    # ======================================================

    targets_baru = []

    for target_item in targets:

        item = dict(target_item)

        hasil = get_target_progress(
            item,
            item["terkumpul"]
        )

        item["progress"] = hasil["progress"]
        item["sisa"] = hasil["sisa"]

        targets_baru.append(item)


    targets = targets_baru


    # ======================================================
    # STATISTIK TARGET
    # ======================================================

    total_target = len(targets)

    total_nominal = sum(
        target_item["nominal_target"]
        for target_item in targets
    )

    total_terkumpul = sum(
        target_item["terkumpul"]
        for target_item in targets
    )

    total_sisa = sum(
        target_item["sisa"]
        for target_item in targets
    )


    conn.close()


    return render_template(

        "target.html",

        targets=targets,

        total_target=total_target,
        total_nominal=total_nominal,
        total_terkumpul=total_terkumpul,
        total_sisa=total_sisa

    )

# ==========================================================
# EDIT TARGET
# Hanya boleh mengedit target milik user sendiri
# ==========================================================

@app.route("/target/edit", methods=["POST"])
def edit_target():

    conn = get_db()

    conn.execute("""
        UPDATE target_tabungan
        SET
            nama_target = %s,
            nominal_target = %s,
            terkumpul = %s,
            tanggal_target = %s
        WHERE id = %s
        AND user_id = %s
    """, (

        request.form["nama_target"],
        int(request.form["nominal_target"]),
        int(request.form.get("terkumpul") or 0),
        request.form["tanggal_target"],

        int(request.form["id"]),

        session["user_id"]

    ))

    conn.commit()
    conn.close()

    flash(
        "Target berhasil diperbarui.",
        "success"
    )

    return redirect("/target")

# ==========================================================
# HAPUS TARGET
# Hanya boleh menghapus target milik user sendiri
# ==========================================================

@app.route("/target/hapus", methods=["POST"])
def hapus_target():

    conn = get_db()

    conn.execute("""
        DELETE FROM target_tabungan
        WHERE id = %s
        AND user_id = %s
    """, (

        int(request.form["id"]),

        session["user_id"]

    ))

    conn.commit()
    conn.close()

    flash(
        "Target berhasil dihapus.",
        "success"
    )

    return redirect("/target")

# ==========================================================
# HALAMAN TRANSAKSI
# ==========================================================

@app.route("/transaksi")
def transaksi():

    # ======================================================
    # PARAMETER
    # ======================================================

    keyword = request.args.get("keyword", "").strip()
    tipe = request.args.get("tipe", "")
    kategori = request.args.get("kategori", "")
    tanggal_awal = request.args.get("tanggal_awal", "")
    tanggal_akhir = request.args.get("tanggal_akhir", "")

    page = request.args.get("page", 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    conn = get_db()

    # ======================================================
    # QUERY DASAR
    # ======================================================

    where = [
        "user_id = %s"
    ]

    params = [
        session["user_id"]
    ]

    if keyword:
        where.append("(keterangan LIKE %s OR kategori LIKE %s OR tipe LIKE %s)")
        params.extend([
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        ])

    if tipe:
        where.append("tipe = %s")
        params.append(tipe)

    if kategori:
        where.append("kategori = %s")
        params.append(kategori)

    if tanggal_awal:
        where.append("tanggal >= %s")
        params.append(tanggal_awal)

    if tanggal_akhir:
        where.append("tanggal <= %s")
        params.append(tanggal_akhir)

    where_sql = ""

    if where:
        where_sql = " WHERE " + " AND ".join(where)

    # ======================================================
    # HITUNG TOTAL DATA
    # ======================================================

    total_data = conn.execute(
        f"""
        SELECT COUNT(*) AS total
        FROM transaksi
        {where_sql}
        """,
        params
    ).fetchone()["total"]

    # ======================================================
    # TOTAL HALAMAN
    # ======================================================

    import math

    total_page = max(1, math.ceil(total_data / per_page))

    # ======================================================
    # AMBIL DATA
    # ======================================================

    data = conn.execute(
        f"""
        SELECT *
        FROM transaksi
        {where_sql}
        ORDER BY tanggal DESC, id DESC
        LIMIT %s
        OFFSET %s
        """,
        params + [per_page, offset]

    ).fetchall()

    # ======================================================
    # DAFTAR KATEGORI
    # ======================================================
    daftar_kategori = conn.execute("""
        SELECT id, nama, tipe
        FROM kategori
        WHERE user_id = %s
        ORDER BY tipe, nama
    """, (
        session["user_id"],
    )).fetchall()

    conn.close()

    # ======================================================
    # TAMPILKAN
    # ======================================================

    return render_template(

        "transaksi.html",
        data=data,
        keyword=keyword,
        tipe=tipe,
        kategori=kategori,
        daftar_kategori=daftar_kategori,
        tanggal_awal=tanggal_awal,
        tanggal_akhir=tanggal_akhir,
        page=page,
        total_page=total_page,
        today=date.today().strftime("%Y-%m-%d")

    )

# ==========================================================
# ROUTE HAPUS TRANSAKSI
# Hanya bisa menghapus transaksi milik user yang login
# ==========================================================

@app.route("/hapus/<int:id>", methods=["POST"])
def hapus(id):

    conn = get_db()

    cursor = conn.execute("""
        DELETE FROM transaksi
        WHERE id = %s
        AND user_id = %s
    """, (
        id,
        session["user_id"]
    ))

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:

        flash(
            "Transaksi tidak ditemukan atau bukan milik akun Anda.",
            "error"
        )

        return redirect(url_for("transaksi"))

    flash(
        "Transaksi berhasil dihapus.",
        "success"
    )

    return redirect(url_for("transaksi"))

# ==========================================================
# HALAMAN LAPORAN
# ==========================================================

@app.route("/laporan")
def laporan():

    conn = get_db()

    # ==========================================================
    # PARAMETER FILTER
    # ==========================================================

    tanggal_awal = request.args.get("tanggal_awal", "")
    tanggal_akhir = request.args.get("tanggal_akhir", "")
    kategori_filter = request.args.get("kategori", "")
    tipe = request.args.get("tipe", "")

    # ==========================================================
    # PAGINATION
    # ==========================================================

    page = request.args.get("page", 1, type=int)

    per_page = 8

    offset = (page - 1) * per_page

    # ==========================================================
    # QUERY FILTER
    # Hanya mengambil transaksi milik user yang sedang login
    # ==========================================================

    where = [
        "user_id = %s"
    ]

    params = [
        session["user_id"]
    ]

    if tanggal_awal:
        where.append("tanggal >= %s")
        params.append(tanggal_awal)

    if tanggal_akhir:
        where.append("tanggal <= %s")
        params.append(tanggal_akhir)

    if kategori_filter:
        where.append("kategori = %s")
        params.append(kategori_filter)

    if tipe:
        where.append("tipe = %s")
        params.append(tipe)

    where_sql = ""

    if where:
        where_sql = " WHERE " + " AND ".join(where)

    # ==========================================================
    # HITUNG TOTAL DATA SESUAI FILTER
    # ==========================================================

    total_data = conn.execute(
        f"""
        SELECT COUNT(*) AS total
        FROM transaksi
        {where_sql}
        """,
        params
    ).fetchone()["total"]

    # ==========================================================
    # HITUNG TOTAL HALAMAN
    # ==========================================================

    import math

    total_page = max(
        1,
        math.ceil(total_data / per_page)
    )

    # Kalau page melebihi halaman terakhir
    if page > total_page:
        page = total_page
        offset = (page - 1) * per_page

    # ==========================================================
    # AMBIL DATA UNTUK HALAMAN AKTIF
    # ==========================================================

    data = conn.execute(
        f"""
        SELECT *
        FROM transaksi
        {where_sql}
        ORDER BY tanggal DESC, id DESC
        LIMIT %s
        OFFSET %s
        """,
        params + [per_page, offset]
    ).fetchall()

    # ==========================================================
    # SUMMARY
    # ==========================================================
    # Summary dihitung dari SEMUA data yang sesuai filter,
    # bukan hanya data pada halaman aktif.

    summary_data = conn.execute(
        f"""
        SELECT tipe, nominal
        FROM transaksi
        {where_sql}
        """,
        params
    ).fetchall()

    pemasukan = sum(
        row["nominal"]
        for row in summary_data
        if row["tipe"] == "Pemasukan"
    )

    pengeluaran = sum(
        row["nominal"]
        for row in summary_data
        if row["tipe"] == "Pengeluaran"
    )

    saldo = pemasukan - pengeluaran

    jumlah_transaksi = len(summary_data)

    # ==========================================================
    # DAFTAR KATEGORI
    # ==========================================================

    daftar_kategori = conn.execute("""
        SELECT DISTINCT kategori
        FROM transaksi
        ORDER BY kategori
    """).fetchall()

    # ==========================================================
    # GRAFIK BULANAN
    # Mengikuti filter laporan dan user yang sedang login
    # ==========================================================

    chart = conn.execute(
        f"""
        SELECT
            TO_CHAR(tanggal::date, 'MM') AS bulan,

            SUM(
                CASE
                    WHEN tipe = 'Pemasukan'
                    THEN nominal
                    ELSE 0
                END
            ) AS pemasukan,

            SUM(
                CASE
                    WHEN tipe = 'Pengeluaran'
                    THEN nominal
                    ELSE 0
                END
            ) AS pengeluaran

        FROM transaksi

        {where_sql}

        GROUP BY bulan

        ORDER BY bulan
        """,
        params
    ).fetchall()
    
    bulan_chart = []
    pemasukan_chart = []
    pengeluaran_chart = []
    
    nama_bulan = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "Mei",
    "Jun",
    "Jul",
    "Agu",
    "Sep",
    "Okt",
    "Nov",
    "Des"
    
    ]
    
    for row in chart:
        
        bulan_chart.append(
        nama_bulan[int(row["bulan"]) - 1]
    )
        pemasukan_chart.append(
        row["pemasukan"] or 0
    )
        pengeluaran_chart.append(
        row["pengeluaran"] or 0
    )
        
    # ==========================================================
    # GRAFIK KATEGORI
    # Mengikuti filter laporan
    # ==========================================================

    chart_where = []
    chart_params = []


    # ==========================================================
    # FILTER TANGGAL
    # ==========================================================

    if tanggal_awal:
        chart_where.append("tanggal >= %s")
        chart_params.append(tanggal_awal)

    if tanggal_akhir:
        chart_where.append("tanggal <= %s")
        chart_params.append(tanggal_akhir)


    # ==========================================================
    # FILTER KATEGORI
    # ==========================================================

    if kategori_filter:
        chart_where.append("kategori = %s")
        chart_params.append(kategori_filter)


    # ==========================================================
    # FILTER TIPE
    # ==========================================================

    if tipe:
        chart_where.append("tipe = %s")
        chart_params.append(tipe)


    # ==========================================================
    # DEFAULT
    # Jika tidak ada filter kategori dan tipe,
    # tampilkan PENGELUARAN saja.
    # ==========================================================

    if not kategori_filter and not tipe:
        
        chart_where.append("tipe = %s")
        chart_params.append("Pengeluaran")


    # ==========================================================
    # BUAT WHERE SQL
    # ==========================================================

    chart_where_sql = ""

    if chart_where:

        chart_where_sql = (
            " WHERE " + " AND ".join(chart_where)
        )


    # ==========================================================
    # GRAFIK KATEGORI
    # Mengikuti filter laporan dan user yang sedang login
    # ==========================================================

    kategori_chart_data = conn.execute(
        f"""
        SELECT
            kategori,
            SUM(nominal) AS total

        FROM transaksi

        {where_sql}

        AND tipe = 'Pengeluaran'

        GROUP BY kategori

        ORDER BY total DESC
        """,
        params
    ).fetchall()


    # ==========================================================
    # DATA UNTUK JAVASCRIPT
    # ==========================================================

    kategori_chart = []
    nominal_chart = []


    for row in kategori_chart_data:

        kategori_chart.append(
            row["kategori"]
        )

        nominal_chart.append(
            row["total"] or 0
        )

    # ==========================================================
    # TUTUP DATABASE
    # ==========================================================

    conn.close()

    # ==========================================================
    # TAMPILKAN
    # ==========================================================

    return render_template(
        "laporan.html",

        today=date.today().strftime("%Y-%m-%d"),

        # Data tabel
        data=data,

        # Summary
        pemasukan=pemasukan,
        pengeluaran=pengeluaran,
        saldo=saldo,
        jumlah_transaksi=jumlah_transaksi,

        # Filter
        daftar_kategori=daftar_kategori,
        tanggal_awal=tanggal_awal,
        tanggal_akhir=tanggal_akhir,
        kategori=kategori_filter,
        tipe=tipe,

        # Grafik bulanan
        bulan_chart=bulan_chart,
        pemasukan_chart=pemasukan_chart,
        pengeluaran_chart=pengeluaran_chart,

        # Grafik kategori
        kategori_chart=kategori_chart,
        nominal_chart=nominal_chart,

        # Pagination
        page=page,
        total_page=total_page
    )

# ==========================================================
# EXPORT PDF
# ==========================================================

@app.route("/laporan/pdf")
def export_pdf():

    conn = get_db()
    data = conn.execute("""

        SELECT
            tanggal,
            keterangan,
            kategori,
            tipe,
            nominal
        FROM transaksi
        WHERE user_id = %s
        ORDER BY tanggal DESC

    """, (
        session["user_id"],
    )).fetchall()

    conn.close()

    pdf = SimpleDocTemplate(

        "laporan_keuangan.pdf"

    )

    styles = getSampleStyleSheet()

    elements = []

    elements.append(

        Paragraph(

            "Laporan Keuangan KEUVIA",

            styles["Heading1"]

        )

    )

    table_data = [

        [

            "Tanggal",

            "Keterangan",

            "Kategori",

            "Tipe",

            "Nominal"

        ]

    ]

    for row in data:

        table_data.append([

            row["tanggal"],

            row["keterangan"],

            row["kategori"],

            row["tipe"],

            f'Rp {row["nominal"]:,}'.replace(",", ".")

        ])

    table = Table(table_data)
    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.blue),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("GRID",(0,0),(-1,-1),1,colors.grey),

            ("BACKGROUND",(0,1),(-1,-1),colors.beige),

            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

            ("BOTTOMPADDING",(0,0),(-1,0),10),

        ])

    )
            
    elements.append(table)

    pdf.build(elements)

    return send_file(

        "laporan_keuangan.pdf",

        as_attachment=True

    )

# ==========================================================
# GANTI PASSWORD
# ==========================================================

@app.route("/ganti-password", methods=["GET", "POST"])
def ganti_password():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        password_lama = request.form["password_lama"]
        password_baru = request.form["password_baru"]
        konfirmasi = request.form["konfirmasi"]

        conn = get_db()

        user = conn.execute("""
            SELECT *
            FROM users
            WHERE id = %s
        """, (session["user_id"],)).fetchone()

        # Cek password lama
        if not user or not check_password_hash(
            user["password"],
            password_lama
        ):

            conn.close()

            flash(
                "Password lama salah.",
                "error"
            )

            return redirect("/ganti-password")

        # Cek password baru
        if password_baru != konfirmasi:

            conn.close()

            flash(
                "Konfirmasi password tidak sama.",
                "error"
            )

            return redirect("/ganti-password")

        # Minimal 6 karakter
        if len(password_baru) < 6:

            conn.close()

            flash(
                "Password baru minimal 6 karakter.",
                "error"
            )

            return redirect("/ganti-password")

        # Buat hash password baru
        password_hash = generate_password_hash(
            password_baru
        )

        conn.execute("""
            UPDATE users
            SET password = %s
            WHERE id = %s
        """, (
            password_hash,
            session["user_id"]
        ))

        conn.commit()
        conn.close()

        flash(
            "Password berhasil diubah.",
            "success"
        )

        return redirect("/profil")

    return render_template(
        "ganti_password.html",
        today=date.today().strftime("%Y-%m-%d")
    )


# ==========================================================
# PROFIL
# ==========================================================

@app.route("/profil")
def profil():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()

    user = conn.execute("""
        SELECT id, username
        FROM users
        WHERE id = %s
    """, (session["user_id"],)).fetchone()

    conn.close()

    return render_template(
        "profil.html",
        user=user,
        today=date.today().strftime("%Y-%m-%d")
    )

# ==========================================================
# MAIN PROGRAM
# ==========================================================

if __name__ == "__main__":

    init_db()

    app.run(

        debug=True

    )