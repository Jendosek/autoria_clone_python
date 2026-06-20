document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('[data-show-settings]')) {
        document.querySelectorAll('.cabinet-content > div').forEach(function(d) { d.classList.remove('is-active'); });
        document.getElementById('tab-settings').classList.add('is-active');
        document.querySelectorAll('.cab-nav__item[data-tab]').forEach(function(a) { a.classList.remove('cab-nav__item--active'); });
        var navItem = document.querySelector('.cab-nav__item[data-tab="settings"]');
        if (navItem) navItem.classList.add('cab-nav__item--active');
    }
});

function confirmDelete() {
    if (confirm('Ви впевнені що хочете видалити акаунт? Цю дію складно скасувати.')) {
        if (confirm('Останнє попередження! Натисніть OK щоб підтвердити видалення.')) {
            document.getElementById('deleteForm').submit();
        }
    }
}