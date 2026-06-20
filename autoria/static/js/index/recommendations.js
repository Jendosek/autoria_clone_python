var INITIAL_COUNT = 6;
var LOAD_MORE_COUNT = 3;
var visibleCount = 0;

document.addEventListener('DOMContentLoaded', function() {
    var cards = document.querySelectorAll('#recsGrid [data-card]');
    var total = cards.length;

    cards.forEach(function(card) {
        card.style.display = 'none';
    });

    visibleCount = Math.min(INITIAL_COUNT, total);
    for (var i = 0; i < visibleCount; i++) {
        cards[i].style.display = '';
    }

    updateMoreButton();
});

function showMore() {
    var cards = document.querySelectorAll('#recsGrid [data-card]');
    var total = cards.length;
    var newCount = Math.min(visibleCount + LOAD_MORE_COUNT, total);

    for (var i = visibleCount; i < newCount; i++) {
        cards[i].style.display = '';
    }

    visibleCount = newCount;
    updateMoreButton();
}

function updateMoreButton() {
    var cards = document.querySelectorAll('#recsGrid [data-card]');
    var btn = document.getElementById('recsMoreWrap');
    if (visibleCount >= cards.length) {
        btn.style.display = 'none';
    } else {
        btn.style.display = '';
    }
}

function hideCard(btn) {
    var card = btn.closest('[data-card]');
    card.querySelector('.car-card__visual').style.display = 'none';
    card.querySelector('.car-card__hidden').style.display = 'block';
}

function unhideCard(btn) {
    var card = btn.closest('[data-card]');
    card.querySelector('.car-card__visual').style.display = '';
    card.querySelector('.car-card__hidden').style.display = 'none';
}

function toggleFav(btn, carId) {
    fetch('/api/favorite/toggle/' + carId + '/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(function(r) {
        if (r.status === 401) {
            window.location.href = '/login/';
            return;
        }
        return r.json();
    })
    .then(function(data) {
        if (!data) return;
        if (data.status === 'added') {
            btn.classList.add('is-liked');
            showToast('Пропозицію додано до Обраного');
        } else if (data.status === 'removed') {
            btn.classList.remove('is-liked');
            showToast('Пропозицію видалено з Обраного');
        }
    });
}

function getCookie(name) {
    var value = '; ' + document.cookie;
    var parts = value.split('; ' + name + '=');
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function showToast(message) {
    var toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.add('show');
    clearTimeout(toast._timer);
    toast._timer = setTimeout(function() { toast.classList.remove('show'); }, 2500);
}