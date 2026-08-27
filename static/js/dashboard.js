/*==========================================================
DASHBOARD JAVASCRIPT
Finance Dashboard
============================================================*/

/*==========================================================
BAR CHART
Pemasukan vs Pengeluaran
============================================================*/

const incomeExpenseChart = document.getElementById("incomeExpenseChart");

if (incomeExpenseChart) {
  new Chart(incomeExpenseChart, {
    type: "bar",
    data: {
      labels: bulanChart,
      datasets: [
        {
          label: "Pemasukan",
          data: pemasukanChart,
          backgroundColor: "#90CAF9",
          borderColor: "#90CAF9",
          borderWidth: 0,
          borderRadius: 8,
        },

        {
          label: "Pengeluaran",
          data: pengeluaranChart,
          backgroundColor: "#F8A5B5",
          borderColor: "#F8A5B5",
          borderWidth: 0,
          borderRadius: 8,
        },
      ],
    },

    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: "bottom",

          labels: {
            usePointStyle: true,
            padding: 20,
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

      scales: {
        x: {
          grid: {
            display: false,
          },
        },

        y: {
          beginAtZero: true,

          ticks: {
            callback: function (value) {
              return "Rp " + value.toLocaleString("id-ID");
            },
          },
        },
      },
    },
  });
}

/*==========================================================
DONUT CHART
Kategori Pengeluaran
Warna kategori otomatis & konsisten
============================================================*/

const kategoriChart = document.getElementById("kategoriChart");

if (kategoriChart) {
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
    Warna tambahan untuk kategori baru
  */

  const warnaKategoriTambahan = ["#9966FF", "#7BC043", "#E67E22", "#8E44AD", "#16A085", "#C9CBCF", "#3498DB", "#E91E63", "#9C27B0", "#009688"];

  /*
    Menentukan warna berdasarkan nama kategori
  */

  function getWarnaKategori(namaKategori) {
    /*
      Kalau kategori sudah memiliki
      warna khusus, gunakan warna tersebut.
    */

    if (warnaKategoriTetap[namaKategori]) {
      return warnaKategoriTetap[namaKategori];
    }

    /*
      Kalau kategori baru,
      buat warna berdasarkan nama kategorinya.
    */

    let hash = 0;

    for (let i = 0; i < namaKategori.length; i++) {
      hash = namaKategori.charCodeAt(i) + ((hash << 5) - hash);
    }

    const index = Math.abs(hash) % warnaKategoriTambahan.length;

    return warnaKategoriTambahan[index];
  }

  /*
    Membuat warna untuk setiap kategori
  */

  const warnaDonut = kategori.map((namaKategori) => getWarnaKategori(namaKategori));

  /*
    Membuat Donut Chart
  */

  new Chart(kategoriChart, {
    type: "doughnut",

    data: {
      labels: kategori,

      datasets: [
        {
          data: nominal,

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
  });
}
