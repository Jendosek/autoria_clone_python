/* Генерація років */
(function initYears() {
    var select = document.getElementById('yearSelect');
    if (!select) return;
    select.innerHTML = '<option value="">Оберіть</option>';
    for (var y = 2026; y >= 1900; y--) {
        select.innerHTML += '<option value="' + y + '">' + y + '</option>';
    }
})();

/* Валідація обов'язкових полів */
function validateInfoForm() {
    var rows = document.querySelectorAll('#infoForm .info-row[data-required]');
    var valid = true;
    rows.forEach(function(row) {
        var field = row.querySelector('select, input');
        if (!field.value) {
            row.classList.add('has-error');
            valid = false;
        } else {
            row.classList.remove('has-error');
        }
    });
    return valid;
}

/* Зняття помилки при зміні */
document.querySelectorAll('#infoForm select, #infoForm input').forEach(function(field) {
    field.addEventListener('change', function() {
        var row = this.closest('.info-row');
        if (row && this.value) row.classList.remove('has-error');
    });
});

function submitListing() {
    var agree = document.getElementById('agreeTerms');
    if (!agree.checked) {
        alert('Прийміть умови угоди');
        return;
    }
    if (!validateInfoForm()) {
        return;
    }
    window.location.href = '/cabinet/';
}