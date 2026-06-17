function toggleListingsFilter() {
    document.getElementById('listingsFilter').classList.toggle('is-open');
}

function toggleSelectAll() {
    var checked = document.getElementById('selectAll').checked;
    document.querySelectorAll('.listing-checkbox').forEach(function(cb) { cb.checked = checked; });
}