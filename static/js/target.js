/*==========================================================
TARGET MODAL
==========================================================*/

const modal = document.getElementById("modalTarget");

const btnTambah = document.getElementById("btnTambahTarget");

const closeModal = document.querySelector(".close-modal");

const form = document.getElementById("targetForm");

const deleteModal = document.getElementById("deleteModal");

const cancelDelete = document.getElementById("cancelDelete");

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
EDIT TARGET
==========================================================*/

document.querySelectorAll(".btn-edit-target").forEach((button) => {
  button.addEventListener("click", () => {
    console.log("Klik :", button.dataset.nama);

    modal.style.display = "flex";

    form.action = "/target/edit";

    document.getElementById("target_id").value = button.dataset.id;

    document.getElementById("nama_target").value = button.dataset.nama;

    document.getElementById("nominal_target").value = button.dataset.target;

    document.getElementById("terkumpul").value = button.dataset.terkumpul;

    document.getElementById("tanggal_target").value = button.dataset.tanggal;
  });
});
/*document.querySelectorAll(".btn-edit-target").forEach((button) => {
  button.addEventListener("click", () => {
    modal.style.display = "flex";

    form.action = "/target/edit";

    document.getElementById("target_id").value = button.dataset.id;

    document.getElementById("nama_target").value = button.dataset.nama;

    document.getElementById("nominal_target").value = button.dataset.target;

    document.getElementById("terkumpul").value = button.dataset.terkumpul;

    document.getElementById("tanggal_target").value = button.dataset.tanggal;
  });
});
*/
/*==========================================================
TAMBAH TARGET
==========================================================*/

btnTambah.onclick = () => {
  modal.style.display = "flex";

  form.action = "/target";

  form.reset();

  document.getElementById("target_id").value = "";
};

/*==========================================================
HAPUS TARGET
==========================================================*/

document.querySelectorAll(".btn-delete-target").forEach((button) => {
  button.addEventListener("click", () => {
    deleteModal.style.display = "flex";

    document.getElementById("delete_target_id").value = button.dataset.id;
  });
});

cancelDelete.onclick = () => {
  deleteModal.style.display = "none";
};

window.addEventListener("click", (e) => {
  if (e.target === deleteModal) {
    deleteModal.style.display = "none";
  }
});
