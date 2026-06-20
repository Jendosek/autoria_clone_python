/* ================================================
   ПЕРЕКЛЮЧЕННЯ ВКЛАДОК
   ================================================ */
function switchAdminTab(e, tab) {
    e.preventDefault();
    document.querySelectorAll('.cabinet-content > div').forEach(function(d) {
        d.classList.remove('is-active');
    });
    var target = document.getElementById('tab-' + tab);
    if (target) target.classList.add('is-active');

    document.querySelectorAll('.cab-nav__item[data-tab]').forEach(function(a) {
        a.classList.remove('cab-nav__item--active');
    });
    var navItem = document.querySelector('.cab-nav__item[data-tab="' + tab + '"]');
    if (navItem) navItem.classList.add('cab-nav__item--active');
}

/* ================================================
   CSRF TOKEN
   ================================================ */
function getCookie(name) {
    var value = '; ' + document.cookie;
    var parts = value.split('; ' + name + '=');
    if (parts.length === 2) return parts.pop().split(';').shift();
}

/* ================================================
   КОРИСТУВАЧІ
   ================================================ */
function banUser(userId) {
    if (!confirm('Заблокувати користувача #' + userId + '?')) return;

    fetch('/api/admin/users/' + userId + '/delete/', {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
        if (data.status === 'banned') {
            var row = document.getElementById('user-row-' + userId);
            row.classList.add('ap-row--banned');

            var status = document.getElementById('user-status-' + userId);
            status.textContent = 'Заблокований';
            status.className = 'ap-status ap-status--banned';

            var actions = row.querySelector('.ap-actions');
            actions.innerHTML = '<button class="ap-btn ap-btn--unban" onclick="unbanUser(' + userId + ')">Розбан</button>';
        }
    });
}

function unbanUser(userId) {
    fetch('/api/admin/users/' + userId + '/unban/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
        if (data.status === 'unbanned') {
            var row = document.getElementById('user-row-' + userId);
            row.classList.remove('ap-row--banned');

            var status = document.getElementById('user-status-' + userId);
            status.textContent = 'Активний';
            status.className = 'ap-status ap-status--active';

            var actions = row.querySelector('.ap-actions');
            actions.innerHTML = '<button class="ap-btn ap-btn--ban" onclick="banUser(' + userId + ')">Бан</button>';
        }
    });
}

/* ================================================
   ОГОЛОШЕННЯ
   ================================================ */
function toggleCar(carId) {
    fetch('/api/admin/cars/' + carId + '/toggle/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
        var row = document.getElementById('car-row-' + carId);
        var status = document.getElementById('car-status-' + carId);
        var toggleBtn = row.querySelector('.ap-btn--toggle');

        if (data.status === 'active') {
            row.classList.remove('ap-row--inactive');
            status.textContent = 'Активне';
            status.className = 'ap-status ap-status--active';
            toggleBtn.textContent = 'Сховати';
        } else {
            row.classList.add('ap-row--inactive');
            status.textContent = 'Приховане';
            status.className = 'ap-status ap-status--banned';
            toggleBtn.textContent = 'Показати';
        }
    });
}

function deleteCar(carId) {
    if (!confirm('Видалити оголошення #' + carId + '? Цю дію не можна скасувати.')) return;

    fetch('/api/admin/cars/' + carId + '/delete/', {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
        if (data.status === 'deleted') {
            var row = document.getElementById('car-row-' + carId);
            row.remove();
        }
    });
}