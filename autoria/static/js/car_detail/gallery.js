var currentIndex = 0;

function getImages() {
    return window.galleryImages || [];
}

function galleryGo(index) {
    var images = getImages();
    if (index < 0 || index >= images.length) return;
    currentIndex = index;

    document.getElementById('galleryImage').src = images[currentIndex];
    document.getElementById('galleryCounter').textContent = (currentIndex + 1) + ' з ' + images.length;

    var thumbs = document.querySelectorAll('.gallery__thumb');
    thumbs.forEach(function(t, i) {
        t.classList.toggle('gallery__thumb--active', i === currentIndex);
    });

    var track = document.getElementById('galleryThumbs');
    var activeThumb = thumbs[currentIndex];
    if (activeThumb && track) {
        var offset = activeThumb.offsetLeft - track.offsetWidth / 2 + activeThumb.offsetWidth / 2;
        track.scrollTo({ left: offset, behavior: 'smooth' });
    }
}

function galleryPrev() {
    galleryGo(currentIndex - 1);
}

function galleryNext() {
    galleryGo(currentIndex + 1);
}

function thumbsScroll(direction) {
    var track = document.getElementById('galleryThumbs');
    track.scrollBy({ left: direction * 300, behavior: 'smooth' });
}