document.addEventListener("DOMContentLoaded", () => {

    const selectAll = document.getElementById("select-all");
    const rowChecks = document.querySelectorAll(".row-check");
    const bulkForm = document.getElementById("bulk-delete-form");
    const hiddenField = document.getElementById("bulk-ids-field");

    // ===========================
    // SELECT ALL
    // ===========================
    if (selectAll) {
        selectAll.addEventListener("change", () => {
            rowChecks.forEach(cb => cb.checked = selectAll.checked);
        });
    }

    // ===========================
    // BULK DELETE
    // ===========================
    if (bulkForm) {
        bulkForm.addEventListener("submit", (e) => {
            const selected = [...rowChecks]
                .filter(cb => cb.checked)
                .map(cb => cb.value);

            if (selected.length === 0) {
                e.preventDefault();
                alert("No vehicles selected.");
                return;
            }

            if (!confirm(`Delete ${selected.length} vehicle(s)?`)) {
                e.preventDefault();
                return;
            }

            hiddenField.value = selected.join(",");
        });
    }
});
