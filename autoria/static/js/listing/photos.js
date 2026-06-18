/* Згортання секцій */
function toggleSection(name) {
    var section = document.querySelector('[data-section="' + name + '"]');
    section.classList.toggle('is-collapsed');
}

/* Завантаження фото */
function handlePhotos(files) {
    var grid = document.getElementById('photosGrid');
    var addBtn = document.getElementById('photosAdd');
    var tip = document.getElementById('photosTip');
    var checklist = document.getElementById('photosChecklist');

    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        if (!file.type.startsWith('image/')) continue;

        var reader = new FileReader();
        reader.onload = (function(isFirst) {
            return function(e) {
                var div = document.createElement('div');
                div.className = 'photos-preview';

                var existing = grid.querySelectorAll('.photos-preview');
                var firstPhoto = existing.length === 0 && isFirst;

                div.innerHTML =
                    '<img src="' + e.target.result + '" alt="">' +
                    '<button class="photos-preview__remove" onclick="removePhoto(this)" type="button">&times;</button>' +
                    (firstPhoto ? '<span class="photos-preview__badge"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> Головне фото</span>' : '');

                grid.insertBefore(div, addBtn);
                updatePhotoState();
            };
        })(i === 0);

        reader.readAsDataURL(file);
    }
}

function removePhoto(btn) {
    var preview = btn.closest('.photos-preview');
    var grid = document.getElementById('photosGrid');
    var wasFirst = preview.querySelector('.photos-preview__badge');
    preview.remove();

    /* Якщо видалили головне фото — перше стає головним */
    if (wasFirst) {
        var first = grid.querySelector('.photos-preview');
        if (first && !first.querySelector('.photos-preview__badge')) {
            var badge = document.createElement('span');
            badge.className = 'photos-preview__badge';
            badge.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> Головне фото';
            first.appendChild(badge);
        }
    }

    updatePhotoState();
}

function updatePhotoState() {
    var grid = document.getElementById('photosGrid');
    var photos = grid.querySelectorAll('.photos-preview');
    var tip = document.getElementById('photosTip');
    var checklist = document.getElementById('photosChecklist');

    if (photos.length > 0) {
        tip.style.display = 'none';
        checklist.style.display = 'block';
    } else {
        tip.style.display = 'flex';
        checklist.style.display = 'none';
    }
}

function toggleColorPicker() {
    var picker = document.getElementById('colorPicker');
    picker.classList.toggle('is-open');
}

function pickColor(swatch) {
    var color = swatch.dataset.color;
    document.getElementById('colorValue').textContent = color;
    document.getElementById('colorValue').classList.add('has-value');
    document.getElementById('colorInput').value = color;

    document.querySelectorAll('.color-swatch').forEach(function(s) { s.classList.remove('is-selected'); });
    swatch.classList.add('is-selected');

    document.getElementById('colorPicker').classList.remove('is-open');
}

document.addEventListener('click', function(e) {
    var picker = document.getElementById('colorPicker');
    if (picker && !picker.contains(e.target)) {
        picker.classList.remove('is-open');
    }
});