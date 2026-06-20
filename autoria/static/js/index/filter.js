const MODELS = {
    'Toyota': ['Camry', 'Corolla', 'RAV4', 'Land Cruiser'],
    'BMW': ['320d', 'X5', 'M3', '520d'],
    'Volkswagen': ['Golf', 'Passat', 'Tiguan', 'Polo'],
    'Chevrolet': ['Lacetti', 'Aveo', 'Bolt EUV', 'Malibu'],
    'Hyundai': ['Tucson', 'Elantra', 'Sonata', 'Kona']
};
let currentCurrency = '$';

function switchTab(clicked) {
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

let selectedBrand = '';
let selectedModels = [];
function selectBrand(radio) {
    selectedBrand = radio.value; selectedModels = [];
    const dd = radio.closest('.dropdown');
    dd.querySelector('.brand-step--brands').style.display = 'none';
    dd.querySelector('.brand-step--models').style.display = 'block';
    dd.querySelector('.brand-search__value').textContent = selectedBrand;
    const modelList = dd.querySelector('.dropdown__list--models');
    modelList.innerHTML = '';
    (MODELS[selectedBrand] || []).forEach(model => {
        const label = document.createElement('label');
        label.className = 'dropdown__option';
        label.innerHTML = `<input type="checkbox" name="model" value="${model}" class="dropdown__checkbox"><span>${model}</span>`;
        modelList.appendChild(label);
    });
    updateBrandValue(dd);
}
function resetBrand() {
    selectedBrand = ''; selectedModels = [];
    const dd = document.querySelector('[data-dropdown="brand"]');
    dd.querySelector('.brand-step--brands').style.display = 'block';
    dd.querySelector('.brand-step--models').style.display = 'none';
    dd.querySelectorAll('[name="brand_select"]').forEach(r => r.checked = false);
    updateBrandValue(dd);
}
function applyBrand() {
    const dd = document.querySelector('[data-dropdown="brand"]');
    selectedModels = [...dd.querySelectorAll('.dropdown__list--models .dropdown__checkbox:checked')].map(cb => cb.value);
    updateBrandValue(dd); dd.classList.remove('is-open');
}
function updateBrandValue(dd) {
    const trigger = dd.querySelector('.dropdown__trigger');
    const valueEl = dd.querySelector('.dropdown__value');
    if (!selectedBrand) { valueEl.textContent = 'Марка, Модель'; trigger.classList.remove('has-label'); }
    else if (selectedModels.length === 0) { valueEl.textContent = selectedBrand + ', Модель'; trigger.classList.add('has-label'); }
    else { valueEl.textContent = selectedBrand + ', ' + selectedModels.join(', '); trigger.classList.add('has-label'); }
}

(function initYears() {
    const fromEl = document.getElementById('yearFrom');
    const toEl = document.getElementById('yearTo');
    for (let y = 2026; y >= 1900; y--) {
        fromEl.innerHTML += `<label class="dropdown__option"><input type="radio" name="year_from" value="${y}" class="dropdown__radio"><span>${y}</span></label>`;
        toEl.innerHTML += `<label class="dropdown__option"><input type="radio" name="year_to" value="${y}" class="dropdown__radio"><span>${y}</span></label>`;
    }
})();
function applyYear() {
    const dd = document.querySelector('[data-dropdown="year"]');
    const from = dd.querySelector('[name="year_from"]:checked');
    const to = dd.querySelector('[name="year_to"]:checked');
    const trigger = dd.querySelector('.dropdown__trigger');
    const valueEl = dd.querySelector('.dropdown__value');
    if (from || to) { const p = []; if (from) p.push('Від ' + from.value); if (to) p.push('до ' + to.value); valueEl.textContent = p.join(' '); trigger.classList.add('has-label'); }
    else { valueEl.textContent = 'Рік випуску'; trigger.classList.remove('has-label'); }
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
    if (from || to) { const p = []; if (from) p.push('Від ' + Number(from).toLocaleString() + ' ' + currentCurrency); if (to) p.push('до ' + Number(to).toLocaleString() + ' ' + currentCurrency); valueEl.textContent = p.join(' '); trigger.classList.add('has-label'); }
    else { valueEl.textContent = 'Вартість'; trigger.classList.remove('has-label'); }
    dd.classList.remove('is-open');
}

function applyCheckbox(name) {
    const dd = document.querySelector(`[data-dropdown="${name}"]`);
    const checked = [...dd.querySelectorAll('.dropdown__checkbox:checked')];
    const trigger = dd.querySelector('.dropdown__trigger');
    const valueEl = dd.querySelector('.dropdown__value');
    const placeholder = dd.querySelector('.dropdown__label').textContent;
    if (checked.length > 0) { valueEl.textContent = checked.map(cb => cb.nextElementSibling.textContent).join(', '); trigger.classList.add('has-label'); }
    else { valueEl.textContent = placeholder; trigger.classList.remove('has-label'); }
    dd.classList.remove('is-open');
}

function clearDropdown(e, name) {
    e.stopPropagation();
    const dd = document.querySelector(`[data-dropdown="${name}"]`);
    const trigger = dd.querySelector('.dropdown__trigger');
    const valueEl = dd.querySelector('.dropdown__value');
    const placeholder = dd.querySelector('.dropdown__label').textContent;
    dd.querySelectorAll('input').forEach(inp => { if (inp.type === 'checkbox' || inp.type === 'radio') inp.checked = false; else inp.value = ''; });
    if (name === 'brand') resetBrand();
    valueEl.textContent = placeholder; trigger.classList.remove('has-label'); dd.classList.remove('is-open');
}