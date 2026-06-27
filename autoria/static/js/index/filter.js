let currentCurrency = '$';
let allBrands = [];
let selectedBrand = '';
let selectedModels = [];


function switchFilterTab(clicked) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('tab--active'));
    clicked.classList.add('tab--active');
}


document.querySelectorAll('.dropdown__trigger').forEach(trigger => {
    trigger.addEventListener('click', function(e) {
        if (e.target.closest('.dropdown__clear')) return;
        const dropdown = this.closest('.dropdown');
        const wasOpen = dropdown.classList.contains('is-open');
        closeAllDropdowns();
        if (!wasOpen) dropdown.classList.add('is-open');
    });
});
document.addEventListener('click', function(e) { if (!e.target.closest('.dropdown')) closeAllDropdowns(); });
document.addEventListener('keydown', function(e) { if (e.key === 'Escape') closeAllDropdowns(); });
function closeAllDropdowns() { document.querySelectorAll('.dropdown.is-open').forEach(d => d.classList.remove('is-open')); }

document.querySelectorAll('[data-dropdown="type"] .dropdown__radio').forEach(radio => {
    radio.addEventListener('change', function() {
        const dd = this.closest('.dropdown');
        dd.querySelector('.dropdown__value').textContent = this.nextElementSibling.textContent;
        dd.classList.remove('is-open');
    });
});

fetch('/api/brands/')
    .then(r => r.json())
    .then(data => { allBrands = data.brands; populateBrands(allBrands); });

function populateBrands(brands) {
    const list = document.querySelector('[data-dropdown="brand"] .dropdown__list--brands');
    if (!list) return;
    list.innerHTML = '';
    brands.forEach(brand => {
        const label = document.createElement('label');
        label.className = 'dropdown__option';
        label.innerHTML = '<input type="radio" name="brand_select" value="' + brand + '" class="dropdown__radio" onchange="selectBrand(this)"><span>' + brand + '</span>';
        list.appendChild(label);
    });
    if (brands.length === 0) {
        list.innerHTML = '<p style="padding:12px;color:#888;font-size:14px;">Марку не знайдено</p>';
    }
}

function filterBrands(input) {
    const query = input.value.toLowerCase();
    const filtered = allBrands.filter(b => b.toLowerCase().includes(query));
    populateBrands(filtered);
}

function selectBrand(radio) {
    selectedBrand = radio.value;
    selectedModels = [];
    const dd = radio.closest('.dropdown');
    dd.querySelector('.brand-step--brands').style.display = 'none';
    dd.querySelector('.brand-step--models').style.display = 'block';
    dd.querySelector('.brand-search__value').textContent = selectedBrand;
    document.getElementById('hiddenBrand').value = selectedBrand;

    fetch('/api/models/' + encodeURIComponent(selectedBrand) + '/')
        .then(r => r.json())
        .then(data => populateFilterModels(data.models));

    updateBrandValue(dd);
}

function populateFilterModels(models) {
    const list = document.querySelector('[data-dropdown="brand"] .dropdown__list--models');
    if (!list) return;
    list.innerHTML = '';
    models.forEach(model => {
        const label = document.createElement('label');
        label.className = 'dropdown__option';
        label.innerHTML = '<input type="checkbox" name="model" value="' + model + '" class="dropdown__checkbox"><span>' + model + '</span>';
        list.appendChild(label);
    });
    if (models.length === 0) {
        list.innerHTML = '<p style="padding:12px;color:#888;font-size:14px;">Моделей не знайдено</p>';
    }
}

function filterModels(input) {
    const query = input.value.toLowerCase();
    fetch('/api/models/' + encodeURIComponent(selectedBrand) + '/')
        .then(r => r.json())
        .then(data => {
            const filtered = data.models.filter(m => m.toLowerCase().includes(query));
            populateFilterModels(filtered);
        });
}

function resetBrand() {
    selectedBrand = '';
    selectedModels = [];
    const dd = document.querySelector('[data-dropdown="brand"]');
    dd.querySelector('.brand-step--brands').style.display = 'block';
    dd.querySelector('.brand-step--models').style.display = 'none';
    dd.querySelectorAll('[name="brand_select"]').forEach(r => r.checked = false);
    var searchInput = dd.querySelector('.brand-search__input');
    if (searchInput) searchInput.value = '';
    document.getElementById('hiddenBrand').value = '';
    populateBrands(allBrands);
    updateBrandValue(dd);
}

function applyBrand() {
    const dd = document.querySelector('[data-dropdown="brand"]');
    selectedModels = [...dd.querySelectorAll('.dropdown__list--models .dropdown__checkbox:checked')].map(cb => cb.value);
    updateBrandValue(dd);
    dd.classList.remove('is-open');
}

function updateBrandValue(dd) {
    const trigger = dd.querySelector('.dropdown__trigger');
    const valueEl = dd.querySelector('.dropdown__value');
    if (!selectedBrand) {
        valueEl.textContent = 'Марка, Модель';
        trigger.classList.remove('has-label');
    } else if (selectedModels.length === 0) {
        valueEl.textContent = selectedBrand + ', Модель';
        trigger.classList.add('has-label');
    } else {
        valueEl.textContent = selectedBrand + ', ' + selectedModels.join(', ');
        trigger.classList.add('has-label');
    }
}

(function initYears() {
    const fromEl = document.getElementById('yearFrom');
    const toEl = document.getElementById('yearTo');
    if (!fromEl || !toEl) return;
    for (let y = 2026; y >= 1900; y--) {
        fromEl.innerHTML += '<label class="dropdown__option"><input type="radio" name="year_from" value="' + y + '" class="dropdown__radio"><span>' + y + '</span></label>';
        toEl.innerHTML += '<label class="dropdown__option"><input type="radio" name="year_to" value="' + y + '" class="dropdown__radio"><span>' + y + '</span></label>';
    }
})();

function applyYear() {
    const dd = document.querySelector('[data-dropdown="year"]');
    const from = dd.querySelector('[name="year_from"]:checked');
    const to = dd.querySelector('[name="year_to"]:checked');
    const trigger = dd.querySelector('.dropdown__trigger');
    const valueEl = dd.querySelector('.dropdown__value');
    if (from || to) {
        const p = [];
        if (from) p.push('Від ' + from.value);
        if (to) p.push('до ' + to.value);
        valueEl.textContent = p.join(' ');
        trigger.classList.add('has-label');
    } else {
        valueEl.textContent = 'Рік випуску';
        trigger.classList.remove('has-label');
    }
    dd.classList.remove('is-open');
}

function switchCurrency(btn, currency) {
    currentCurrency = currency;
    btn.closest('.currency-tabs').querySelectorAll('.currency-tab').forEach(t => t.classList.remove('currency-tab--active'));
    btn.classList.add('currency-tab--active');
}

function applyPrice() {
    const dd = document.querySelector('[data-dropdown="price"]');
    const from = document.getElementById('priceFrom').value;
    const to = document.getElementById('priceTo').value;
    const trigger = dd.querySelector('.dropdown__trigger');
    const valueEl = dd.querySelector('.dropdown__value');
    if (from || to) {
        const p = [];
        if (from) p.push('Від ' + Number(from).toLocaleString() + ' ' + currentCurrency);
        if (to) p.push('до ' + Number(to).toLocaleString() + ' ' + currentCurrency);
        valueEl.textContent = p.join(' ');
        trigger.classList.add('has-label');
    } else {
        valueEl.textContent = 'Вартість';
        trigger.classList.remove('has-label');
    }
    dd.classList.remove('is-open');
}

function applyCheckbox(name) {
    const dd = document.querySelector('[data-dropdown="' + name + '"]');
    const checked = [...dd.querySelectorAll('.dropdown__checkbox:checked')];
    const trigger = dd.querySelector('.dropdown__trigger');
    const valueEl = dd.querySelector('.dropdown__value');
    const placeholder = dd.querySelector('.dropdown__label').textContent;
    if (checked.length > 0) {
        valueEl.textContent = checked.map(cb => cb.nextElementSibling.textContent).join(', ');
        trigger.classList.add('has-label');
    } else {
        valueEl.textContent = placeholder;
        trigger.classList.remove('has-label');
    }
    dd.classList.remove('is-open');
}

function clearDropdown(e, name) {
    e.stopPropagation();
    const dd = document.querySelector('[data-dropdown="' + name + '"]');
    const trigger = dd.querySelector('.dropdown__trigger');
    const valueEl = dd.querySelector('.dropdown__value');
    const placeholder = dd.querySelector('.dropdown__label').textContent;
    dd.querySelectorAll('input').forEach(inp => {
        if (inp.type === 'checkbox' || inp.type === 'radio') inp.checked = false;
        else inp.value = '';
    });
    if (name === 'brand') resetBrand();
    valueEl.textContent = placeholder;
    trigger.classList.remove('has-label');
    dd.classList.remove('is-open');
}

function clearAllFilters() {
    document.querySelectorAll('.dropdown').forEach(dd => {
        dd.querySelectorAll('input').forEach(inp => {
            if (inp.type === 'checkbox' || inp.type === 'radio') inp.checked = false;
            else if (inp.type !== 'hidden') inp.value = '';
        });
        const trigger = dd.querySelector('.dropdown__trigger');
        const valueEl = dd.querySelector('.dropdown__value');
        const placeholder = dd.querySelector('.dropdown__label');
        if (placeholder && valueEl) {
            valueEl.textContent = placeholder.textContent;
            trigger.classList.remove('has-label');
        }
    });
    resetBrand();
    window.location.href = '/';
}