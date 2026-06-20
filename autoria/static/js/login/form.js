/* ================================================
   ПОКАЗАТИ / СХОВАТИ ПАРОЛЬ
   ================================================ */
function togglePassword(inputId, btn) {
    var input = document.getElementById(inputId);
    var isPassword = input.type === 'password';
    input.type = isPassword ? 'text' : 'password';

    btn.innerHTML = isPassword
        ? '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#aaa" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>'
        : '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#aaa" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>';
}

/* ================================================
   ПЕРЕКЛЮЧЕННЯ ФОРМ
   ================================================ */
function switchToRegister(e) {
    e.preventDefault();
    document.getElementById('authLogin').style.display = 'none';
    document.getElementById('authRegister').style.display = 'block';
}

function switchToLogin(e) {
    e.preventDefault();
    document.getElementById('authRegister').style.display = 'none';
    document.getElementById('authLogin').style.display = 'block';
}

/* ================================================
   ЧЕКБОКС УМОВ
   ================================================ */
function toggleTerms() {
    var checked = document.getElementById('termsCheck').checked;
    var btn = document.getElementById('regSubmit');
    var socials = document.getElementById('regSocials');

    if (checked) {
        btn.disabled = false;
        btn.classList.add('is-active');
        socials.classList.add('is-active');
        // Розблоковуємо Google посилання
        var googleLink = socials.querySelector('a.auth-social');
        if (googleLink) {
            googleLink.style.pointerEvents = 'auto';
            googleLink.style.opacity = '1';
        }
    } else {
        btn.disabled = true;
        btn.classList.remove('is-active');
        socials.classList.remove('is-active');
        var googleLink = socials.querySelector('a.auth-social');
        if (googleLink) {
            googleLink.style.pointerEvents = 'none';
            googleLink.style.opacity = '0.5';
        }
    }
}

/* ================================================
   ПОКАЗ ФОРМИ РЕЄСТРАЦІЇ ПРИ ПОМИЛЦІ
   ================================================ */
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('[data-show-register]')) {
        document.getElementById('authLogin').style.display = 'none';
        document.getElementById('authRegister').style.display = 'block';
    }
});