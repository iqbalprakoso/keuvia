/*=========================================
BAR CHART
=========================================*/

new Chart(
  document.getElementById("laporanChart"),

  {
    type: "bar",

    data: {
      labels: bulanChart,

      datasets: [
        {
          label: "Pemasukan",

          data: pemasukanChart,

          borderRadius: 8,
        },

        {
          label: "Pengeluaran",

          data: pengeluaranChart,

          borderRadius: 8,
        },
      ],
    },

    options: {
      responsive: true,

      maintainAspectRatio: false,
    },
  }
);

/*=========================================
DONUT
Warna kategori otomatis & konsisten
=========================================*/

/*
  Warna khusus kategori yang sudah digunakan
*/
const warnaKategoriTetap = {
  Tagihan: "#36A2EB",
  Belanja: "#FF6384",
  Makan: "#FF9F40",
  "Pulsa dan Internet": "#FFCD56",
  Transportasi: "#4BC0C0",
};

/*
  Warna cadangan untuk kategori baru
*/
const warnaKategoriTambahan = ["#9966FF", "#FF9F40", "#36A2EB", "#4BC0C0", "#FF6384", "#FFCD56", "#7BC043", "#E67E22", "#8E44AD", "#16A085"];

/*
  Membuat warna berdasarkan nama kategori.

  Jadi:
  Makan → selalu oranye
  Belanja → selalu pink

  Walaupun kategori tersebut sedang difilter
  dan hanya tersisa satu kategori.
*/
function getWarnaKategori(namaKategori) {
  // Kalau kategori sudah punya warna khusus
  if (warnaKategoriTetap[namaKategori]) {
    return warnaKategoriTetap[namaKategori];
  }

  /*
    Untuk kategori baru:
    gunakan nama kategori sebagai dasar
    supaya warnanya konsisten.
  */

  let hash = 0;

  for (let i = 0; i < namaKategori.length; i++) {
    hash = namaKategori.charCodeAt(i) + ((hash << 5) - hash);
  }

  const index = Math.abs(hash) % warnaKategoriTambahan.length;

  return warnaKategoriTambahan[index];
}

/*
  Buat daftar warna sesuai kategori
*/
const warnaDonut = kategoriChart.map((namaKategori) => getWarnaKategori(namaKategori));

/*
  Buat Donut Chart
*/
new Chart(
  document.getElementById("kategoriChart"),

  {
    type: "doughnut",

    data: {
      labels: kategoriChart,

      datasets: [
        {
          data: nominalChart,

          backgroundColor: warnaDonut,

          borderWidth: 0,
        },
      ],
    },

    options: {
      responsive: true,

      maintainAspectRatio: false,

      cutout: "70%",

      plugins: {
        legend: {
          display: true,

          position: "bottom",

          labels: {
            usePointStyle: true,

            pointStyle: "circle",

            padding: 15,
          },
        },

        tooltip: {
          callbacks: {
            label: function (context) {
              return context.label + " : Rp " + context.raw.toLocaleString("id-ID");
            },
          },
        },
      },
    },
  }
);
