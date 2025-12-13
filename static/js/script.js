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
    const preview = document.getElementById("preview");
    preview.innerHTML = "";

    [...event.target.files].forEach(file => {
        const reader = new FileReader();
        reader.onload = e => {
            const col = document.createElement("div");
            col.className = "col-6 col-md-4";

            col.innerHTML = `
                <div class="card shadow-sm">
                    <img src="${e.target.result}" class="img-fluid rounded">
                    <div class="card-body p-2">
                        <small class="text-muted">${file.name}</small>
                    </div>
                </div>
            `;
            preview.appendChild(col);
        };
        reader.readAsDataURL(file);
    });
}