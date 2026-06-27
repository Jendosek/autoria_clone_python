document.addEventListener('DOMContentLoaded', function() {

    var yearSelect = document.getElementById('yearSelect');
    if (yearSelect) {
        yearSelect.innerHTML = '<option value="">Оберіть</option>';
        for (var y = 2026; y >= 1900; y--) {
            yearSelect.innerHTML += '<option value="' + y + '">' + y + '</option>';
        }
    }

    var brandSelect = document.getElementById('listingBrand');
    if (brandSelect) {
        fetch('/api/brands/')
            .then(function(r) { return r.json(); })
            .then(function(data) {
                data.brands.forEach(function(brand) {
                    var opt = document.createElement('option');
                    opt.value = brand;
                    opt.textContent = brand;
                    brandSelect.appendChild(opt);
                });
            });
    }

    document.querySelectorAll('#infoForm select, #infoForm input').forEach(function(field) {
        field.addEventListener('change', function() {
            var row = this.closest('.info-row');
            if (row && this.value) row.classList.remove('has-error');
        });
    });

});

function onBrandChange(select) {
    var brand = select.value;
    var modelSelect = document.getElementById('listingModel');

    if (!brand) {
        modelSelect.innerHTML = '<option value="">Спочатку оберіть марку</option>';
        modelSelect.disabled = true;
        return;
    }

    modelSelect.innerHTML = '<option value="">Завантаження...</option>';
    modelSelect.disabled = true;

    fetch('/api/models/' + encodeURIComponent(brand) + '/')
        .then(function(r) { return r.json(); })
        .then(function(data) {
            modelSelect.innerHTML = '<option value="">Оберіть модель</option>';
            data.models.forEach(function(model) {
                var opt = document.createElement('option');
                opt.value = model;
                opt.textContent = model;
                modelSelect.appendChild(opt);
            });
            modelSelect.disabled = false;
        });
}

function validateInfoForm() {
    var rows = document.querySelectorAll('#infoForm .info-row[data-required]');
    var valid = true;
    rows.forEach(function(row) {
        var field = row.querySelector('select, input');
        if (!field || !field.value) {
            row.classList.add('has-error');
            valid = false;
        } else {
            row.classList.remove('has-error');
        }
    });
    return valid;
}