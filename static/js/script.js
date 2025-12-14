function addClassToInput(className) {
    const input = document.getElementById('selected_classes');
    const classes = input.value
        .split(',')
        .map(c => c.trim())
        .filter(Boolean);

    if (!classes.includes(className)) {
        classes.push(className);
        input.value = classes.join(', ');
    }
}

const clsInput = document.getElementById('selected_classes');

clsInput.addEventListener('focus', function() {
    this.placeholder = 'missing_hole, mouse_bite, spur, short...';
});

clsInput.addEventListener('blur', function() {
    this.placeholder = 'Например: missing_hole, mouse_bite, spur, short';
});

function previewImages(event) {
    const files = event.target.files;
    const preview = document.getElementById("preview");
    const previewCol = document.getElementById("previewCol");
    const formCol = document.getElementById("formCol");
    const mainRow = document.getElementById("mainRow");

    preview.innerHTML = "";

    if (files.length === 0) {
        previewCol.classList.add("d-none");
        formCol.classList.remove("col-lg-5");
        formCol.classList.add("col-lg-6");
        mainRow.classList.add("justify-content-center");
        return;
    }

    previewCol.classList.remove("d-none");

    formCol.classList.remove("col-lg-6");
    formCol.classList.add("col-lg-5");
    previewCol.classList.remove("col-lg-6");
    previewCol.classList.add("col-lg-7");
    mainRow.classList.remove("justify-content-center");

    Array.from(files).forEach(file => {
        if (!file.type.startsWith("image/")) return;

        const reader = new FileReader();
        reader.onload = e => {
            const col = document.createElement("div");
            col.className = "col-6 col-md-4";

            col.innerHTML = `
                <div class="card shadow-sm">
                    <img src="${e.target.result}"
                         class="img-fluid rounded"
                         style="height:160px; object-fit:cover">
                    <div class="card-body p-2">
                        <small class="text-muted d-block text-truncate">
                            ${file.name}
                        </small>
                    </div>
                </div>
            `;

            preview.appendChild(col);
        };
        reader.readAsDataURL(file);
    });
}