/* ==========================================================
   MODAL KATEGORI
========================================================== */

const modalKategori = document.getElementById("modalKategori");

const btnTambahKategori = document.getElementById("btnTambahKategori");

const closeKategori = document.querySelector(".close-kategori");

if (btnTambahKategori && modalKategori) {
  btnTambahKategori.onclick = () => {
    modalKategori.style.display = "flex";
  };
}

if (closeKategori && modalKategori) {
  closeKategori.onclick = () => {
    modalKategori.style.display = "none";
  };
}

window.addEventListener("click", (event) => {
  if (event.target === modalKategori) {
    modalKategori.style.display = "none";
  }
});

/* ==========================================================
   EDIT KATEGORI
========================================================== */

const modalEditKategori = document.getElementById("modalEditKategori");

const formEditKategori = document.getElementById("formEditKategori");

const editNamaKategori = document.getElementById("editNamaKategori");

const editTipeKategori = document.getElementById("editTipeKategori");

const closeEditKategori = document.querySelector(".close-edit-kategori");

const tombolEditKategori = document.querySelectorAll(".btn-edit-kategori");

tombolEditKategori.forEach((button) => {
  button.addEventListener("click", function () {
    const id = this.dataset.id;
    const nama = this.dataset.nama;
    const tipe = this.dataset.tipe;

    editNamaKategori.value = nama;

    editTipeKategori.value = tipe;

    formEditKategori.action = `/kategori/edit/${id}`;

    modalEditKategori.style.display = "flex";
  });
});

if (closeEditKategori) {
  closeEditKategori.addEventListener("click", () => {
    modalEditKategori.style.display = "none";
  });
}

window.addEventListener("click", (event) => {
  if (event.target === modalEditKategori) {
    modalEditKategori.style.display = "none";
  }
});

/* ==========================================================
   HAPUS KATEGORI
========================================================== */

const modalHapusKategori = document.getElementById("modalHapusKategori");

const namaHapusKategori = document.getElementById("namaHapusKategori");

const formHapusKategori = document.getElementById("formHapusKategori");

const btnBatalHapusKategori = document.getElementById("btnBatalHapusKategori");

const closeHapusKategori = document.querySelector(".close-hapus-kategori");

const tombolHapusKategori = document.querySelectorAll(".btn-delete-kategori");

tombolHapusKategori.forEach((button) => {
  button.addEventListener("click", function () {
    const id = this.dataset.id;
    const nama = this.dataset.nama;

    namaHapusKategori.textContent = nama;

    formHapusKategori.action = `/kategori/hapus/${id}`;

    modalHapusKategori.style.display = "flex";
  });
});

if (btnBatalHapusKategori) {
  btnBatalHapusKategori.addEventListener("click", () => {
    modalHapusKategori.style.display = "none";
  });
}

if (closeHapusKategori) {
  closeHapusKategori.addEventListener("click", () => {
    modalHapusKategori.style.display = "none";
  });
}

window.addEventListener("click", (event) => {
  if (event.target === modalHapusKategori) {
    modalHapusKategori.style.display = "none";
  }
});
