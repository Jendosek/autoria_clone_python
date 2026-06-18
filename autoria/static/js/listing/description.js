function updateCharCount() {
    var textarea = document.getElementById('descTextarea');
    var counter = document.getElementById('descChars');
    var remaining = 2000 - textarea.value.length;
    counter.textContent = 'Доступно ' + remaining + ' символів';
}