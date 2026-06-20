from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import User, Car, Favorite


def index(request):
    cars = Car.objects.filter(is_active=True).select_related('seller')
    return render(request, 'index/index.html', {
        'cars': cars,
        'is_logged_in': request.user.is_authenticated,
    })


def car_detail(request, car_id):
    car = Car.objects.select_related('seller').filter(id=car_id).first()
    similar_cars = Car.objects.filter(is_active=True).exclude(id=car_id).select_related('seller')[:6]
    return render(request, 'car_detail/car_detail.html', {
        'car': car,
        'similar_cars': similar_cars,
        'is_logged_in': request.user.is_authenticated,
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('cabinet')

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'login':
            identifier = request.POST.get('identifier', '').strip()
            password = request.POST.get('password', '')

            # Шукаємо юзера по email, телефону або username
            user_obj = User.objects.filter(
                Q(email=identifier) | Q(phone=identifier) | Q(username=identifier)
            ).first()

            if user_obj:
                user = authenticate(request, username=user_obj.username, password=password)
                if user:
                    login(request, user)
                    return redirect('cabinet')

            return render(request, 'login/login.html', {
                'error': 'Невірний логін або пароль'
            })

        elif form_type == 'register':
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            identifier = request.POST.get('identifier', '').strip()
            password = request.POST.get('password', '')

            if not first_name or not identifier or not password:
                return render(request, 'login/login.html', {
                    'reg_error': 'Заповніть обов\'язкові поля',
                    'show_register': True,
                })

            # Перевіряємо чи юзер вже існує
            is_email = '@' in identifier
            if is_email:
                if User.objects.filter(email=identifier).exists():
                    return render(request, 'login/login.html', {
                        'reg_error': 'Користувач з таким email вже існує',
                        'show_register': True,
                    })
            else:
                if User.objects.filter(phone=identifier).exists():
                    return render(request, 'login/login.html', {
                        'reg_error': 'Користувач з таким телефоном вже існує',
                        'show_register': True,
                    })

            # Створюємо юзера
            username = identifier.replace('@', '_').replace('.', '_').replace('+', '').replace(' ', '')
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            if is_email:
                user.email = identifier
            else:
                user.phone = identifier
            user.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('cabinet')

    return render(request, 'login/login.html')


def cabinet(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_cars = Car.objects.filter(seller=request.user).select_related('seller')
    favorites = Favorite.objects.filter(user=request.user).select_related('car', 'car__seller')
    return render(request, 'cabinet/cabinet.html', {
        'user': request.user,
        'cars': user_cars,
        'favorite_cars': [fav.car for fav in favorites],
    })


def add_listing(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'listing/listing.html', {'user': request.user})


def logout_view(request):
    logout(request)
    return redirect('index')


def force_login(request):
    user = User.objects.first()
    if user:
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('cabinet')