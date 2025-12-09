// --- Confirm Modal Logic ---
const modal = document.getElementById("confirm-modal");
const modalText = document.getElementById("confirm-modal-text");
const btnCancel = document.getElementById("confirm-cancel");
const btnOk = document.getElementById("confirm-ok");

window.showConfirm = function(message, callback) {
    modal.classList.add("open");
    modalText.textContent = message;

    btnCancel.onclick = () => modal.classList.remove("open");
    btnOk.onclick = () => {
        modal.classList.remove("open");
        callback();
    };
};
