/*==========================================================
MODAL TAMBAH
==========================================================*/

const modal = document.getElementById("modalTambah");

const btnTambah = document.querySelector(".btn-primary");

const closeModal = document.querySelector(".close-modal");

btnTambah.onclick = () => {
  modal.style.display = "flex";
};

closeModal.onclick = () => {
  modal.style.display = "none";
};

window.onclick = (e) => {
  if (e.target == modal) {
    modal.style.display = "none";
  }
};

/*==========================================================
EDIT TRANSAKSI
==========================================================*/

const modalEdit = document.getElementById("modalEdit");

const closeEdit = document.querySelector(".close-edit");

const editTipe = document.getElementById("editTipe");

const editKategori = document.getElementById("editKategori");

/* ==========================================================
   FILTER KATEGORI EDIT
========================================================== */

function filterKategoriEdit() {
  if (!editTipe || !editKategori) {
    return;
  }

  const tipeDipilih = editTipe.value;

  const options = editKategori.querySelectorAll("option");

  options.forEach((option) => {
    if (option.value === "") {
      option.hidden = false;

      return;
    }

    const tipeKategori = option.dataset.tipe;

    if (tipeKategori === tipeDipilih) {
      option.hidden = false;
    } else {
      option.hidden = true;
    }
  });
}

/* ==========================================================
   BUKA MODAL EDIT
========================================================== */

document.querySelectorAll(".btn-edit").forEach((button) => {
  button.addEventListener("click", () => {
    modalEdit.style.display = "flex";

    /* Tanggal */

    document.getElementById("editTanggal").value = button.dataset.tanggal;

    /* Keterangan */

    document.getElementById("editKeterangan").value = button.dataset.keterangan;

    /* Tipe */

    editTipe.value = button.dataset.tipe;

    /* Filter kategori berdasarkan tipe */

    filterKategoriEdit();

    /* Kategori */

    editKategori.value = button.dataset.kategori;

    /* Nominal */

    document.getElementById("editNominal").value = button.dataset.nominal;

    /* Action */

    document.getElementById("formEdit").action = "/update/" + button.dataset.id;
  });
});

/* ==========================================================
   JIKA TIPE DIUBAH
========================================================== */

if (editTipe) {
  editTipe.addEventListener("change", () => {
    filterKategoriEdit();

    // Reset kategori ketika tipe berubah
    editKategori.value = "";
  });
}

/* ==========================================================
   TUTUP MODAL
========================================================== */

if (closeEdit) {
  closeEdit.onclick = () => {
    modalEdit.style.display = "none";
  };
}

/*==========================================================
HAPUS TRANSAKSI
==========================================================*/

const modalDelete = document.getElementById("modalDelete");

const cancelDelete = document.getElementById("cancelDelete");

document.querySelectorAll(".btn-delete").forEach((button) => {
  button.addEventListener("click", () => {
    modalDelete.style.display = "flex";

    document.getElementById("deleteForm").action = "/hapus/" + button.dataset.id;
  });
});

cancelDelete.onclick = () => {
  modalDelete.style.display = "none";
};

window.addEventListener("click", (e) => {
  if (e.target === modalDelete) {
    modalDelete.style.display = "none";
  }
});

/* ==========================================================
   FILTER KATEGORI BERDASARKAN TIPE TRANSAKSI
========================================================== */

const tipeTransaksi = document.getElementById("tipeTransaksi");
const kategoriTransaksi = document.getElementById("kategoriTransaksi");

function filterKategori() {
  if (!tipeTransaksi || !kategoriTransaksi) {
    return;
  }

  const tipeDipilih = tipeTransaksi.value;

  const options = kategoriTransaksi.querySelectorAll("option");

  options.forEach((option) => {
    // Opsi "Pilih Kategori" selalu ditampilkan
    if (option.value === "") {
      option.hidden = false;
      return;
    }

    // Ambil tipe dari data-tipe
    const tipeKategori = option.dataset.tipe;

    // Tampilkan hanya kategori yang sesuai
    if (tipeKategori === tipeDipilih) {
      option.hidden = false;
    } else {
      option.hidden = true;
    }
  });

  // Reset pilihan kategori
  kategoriTransaksi.value = "";
}

/* Jalankan ketika tipe berubah */

if (tipeTransaksi && kategoriTransaksi) {
  tipeTransaksi.addEventListener("change", filterKategori);

  // Jalankan saat halaman pertama kali dibuka
  filterKategori();
}
