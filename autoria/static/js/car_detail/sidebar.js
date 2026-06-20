function copyVin(vin) {
    navigator.clipboard.writeText(vin).catch(function() {});
}

function getCookie(name) {
    var value = '; ' + document.cookie;
    var parts = value.split('; ' + name + '=');
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function toggleDetailFav(btn, carId) {
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
        } else if (data.status === 'removed') {
            btn.classList.remove('is-liked');
        }
    });
}