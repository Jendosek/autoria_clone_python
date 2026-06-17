/* Сповіщення */
function toggleNotification() {
    document.getElementById('dashNotification').classList.toggle('is-open');
}

/* Зірки */
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