function toggleNotification() {
    document.getElementById('dashNotification').classList.toggle('is-open');
}

(function() {
    var container = document.getElementById('dashStars');
    if (!container) return;
    var stars = [].slice.call(container.querySelectorAll('.dash-star'));
    var fixed = 0;
    container.addEventListener('mouseover', function(e) {
        var s = e.target.closest('.dash-star');
        if (!s) return;
        var v = parseInt(s.dataset.value);
        stars.forEach(function(el) { el.classList.toggle('hovered', parseInt(el.dataset.value) <= v && parseInt(el.dataset.value) > fixed); });
    });
    container.addEventListener('mouseout', function() { stars.forEach(function(el) { el.classList.remove('hovered'); }); });
    container.addEventListener('click', function(e) {
        var s = e.target.closest('.dash-star');
        if (!s) return;
        fixed = parseInt(s.dataset.value);
        stars.forEach(function(el) { el.classList.toggle('active', parseInt(el.dataset.value) <= fixed); el.classList.remove('hovered'); });
    });
})();

function getCookieCab(name) {
    var value = '; ' + document.cookie;
    var parts = value.split('; ' + name + '=');
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function removeFavorite(carId, btn) {
    fetch('/api/favorite/toggle/' + carId + '/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookieCab('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
        if (data.status === 'removed') {
            var card = document.getElementById('fav-card-' + carId);
            if (card) card.remove();
        }
    });
}