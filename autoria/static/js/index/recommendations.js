/* ================================================
   ПАГІНАЦІЯ — показуємо по 6, потім +3
   ================================================ */
var INITIAL_COUNT = 6;
var LOAD_MORE_COUNT = 3;
var visibleCount = 0;

document.addEventListener('DOMContentLoaded', function() {
    var cards = document.querySelectorAll('#recsGrid [data-card]');
    var total = cards.length;

    // Спочатку ховаємо всі
    cards.forEach(function(card) {
        card.style.display = 'none';
    });

    // Показуємо перші 6 (або менше якщо машин мало)
    visibleCount = Math.min(INITIAL_COUNT, total);
    for (var i = 0; i < visibleCount; i++) {
        cards[i].style.display = '';
    }

    // Ховаємо кнопку якщо показали все
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

/* ================================================
   ПРИХОВАТИ / ПОКАЗАТИ КАРТКУ
   ================================================ */
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

/* ================================================
   ОБРАНЕ + ТОСТ
   ================================================ */
function toggleFav(btn) {
    var isLiked = btn.classList.toggle('is-liked');
    showToast(isLiked ? 'Пропозицію додано до Обраного' : 'Пропозицію видалено з Обраного');
}

function showToast(message) {
    var toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.add('show');
    clearTimeout(toast._timer);
    toast._timer = setTimeout(function() { toast.classList.remove('show'); }, 2500);
}