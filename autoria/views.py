from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
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
        # Поки логін по username + password
        # Потім замінимо на телефон/email через allauth
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('cabinet')
        return render(request, 'login/login.html', {'error': 'Невірний логін або пароль'})
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
    # Для тестування — логін як перший юзер
    user = User.objects.first()
    if user:
        login(request, user)
    return redirect('cabinet')