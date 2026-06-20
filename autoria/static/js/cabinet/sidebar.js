function switchTab(e, tab) {
    e.preventDefault();
    document.querySelectorAll('.cabinet-content > div').forEach(function(d) { d.classList.remove('is-active'); });
    var target = document.getElementById('tab-' + tab);
    if (target) target.classList.add('is-active');
    document.querySelectorAll('.cab-nav__item[data-tab]').forEach(function(a) { a.classList.remove('cab-nav__item--active'); });
    var navItem = document.querySelector('.cab-nav__item[data-tab="' + tab + '"]');
    if (navItem) navItem.classList.add('cab-nav__item--active');
}

function toggleExpand(e, name) {
    e.preventDefault();
    var current = document.querySelector('[data-expand="' + name + '"]');
    var wasOpen = current.classList.contains('is-open');
    document.querySelectorAll('.cab-nav__expand').forEach(function(el) { el.classList.remove('is-open'); });
    if (!wasOpen) current.classList.add('is-open');
}