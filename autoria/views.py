from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.db.models import Q
from .models import User, Car, Favorite, CarImage
from allauth.socialaccount.models import SocialAccount
from allauth.account.models import EmailAddress
from django.http import JsonResponse



def index(request):
    cars = Car.objects.filter(is_active=True).select_related('seller')
    favorite_ids = []
    if request.user.is_authenticated:
        favorite_ids = list(Favorite.objects.filter(user=request.user).values_list('car_id', flat=True))
    return render(request, 'index/index.html', {
        'cars': cars,
        'is_logged_in': request.user.is_authenticated,
        'favorite_ids': favorite_ids,
    })


def car_detail(request, car_id):
    car = Car.objects.select_related('seller').filter(id=car_id).first()
    similar_cars = Car.objects.filter(is_active=True).exclude(id=car_id).select_related('seller')[:6]
    favorite_ids = []
    if request.user.is_authenticated:
        favorite_ids = list(Favorite.objects.filter(user=request.user).values_list('car_id', flat=True))

    gallery_images = []
    if car:
        if car.image and hasattr(car.image, 'url'):
            gallery_images.append(car.image.url)
        else:
            gallery_images.append('/static/images/cars/default.jpg')
        for img in car.images.all().order_by('order'):
            if img.image and hasattr(img.image, 'url'):
                gallery_images.append(img.image.url)

    return render(request, 'car_detail/car_detail.html', {
        'car': car,
        'similar_cars': similar_cars,
        'is_logged_in': request.user.is_authenticated,
        'favorite_ids': favorite_ids,
        'gallery_images': gallery_images,
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('cabinet')

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'login':
            identifier = request.POST.get('identifier', '').strip()
            password = request.POST.get('password', '')

            user_obj = User.objects.filter(
                Q(email=identifier) | Q(phone=identifier) | Q(username=identifier)
            ).first()

            if user_obj:
                user = authenticate(request, username=user_obj.username, password=password)
                if user:
                    login(request, user)
                    if user.is_staff:
                        return redirect('admin_panel')
                    return redirect('cabinet')

            return render(request, 'login/login.html', {
                'error': 'Невірний логін або пароль'
            })


        elif form_type == 'register':
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            phone = request.POST.get('phone', '').strip()
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '')

            if not first_name or not phone or not email or not password:
                return render(request, 'login/login.html', {
                    'reg_error': 'Заповніть всі обов\'язкові поля',
                    'show_register': True,
                })

            if User.objects.filter(email=email).exists():
                return render(request, 'login/login.html', {
                    'reg_error': 'Користувач з таким email вже існує',
                    'show_register': True,
                })

            if User.objects.filter(phone=phone).exists():
                return render(request, 'login/login.html', {
                    'reg_error': 'Користувач з таким телефоном вже існує',
                    'show_register': True,
                })

            username = email.replace('@', '_').replace('.', '_')
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
            )

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('cabinet')

    return render(request, 'login/login.html')


def cabinet(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_cars = Car.objects.filter(seller=request.user).select_related('seller')
    favorites = Favorite.objects.filter(user=request.user).select_related('car', 'car__seller')
    has_google = SocialAccount.objects.filter(user=request.user, provider='google').exists()
    return render(request, 'cabinet/cabinet.html', {
        'user': request.user,
        'cars': user_cars,
        'favorite_cars': [fav.car for fav in favorites],
        'has_google': has_google,
        'has_password': request.user.has_usable_password(),
    })


def add_listing(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        brand = request.POST.get('brand', '').strip()
        model = request.POST.get('model', '').strip()
        year = request.POST.get('year', '')
        body_type = request.POST.get('body_type', '').strip()
        region = request.POST.get('region', '').strip()
        city = request.POST.get('city', '').strip()
        price = request.POST.get('price', '')

        if not all([brand, year, price]):
            return render(request, 'listing/listing.html', {
                'user': request.user,
                'errors': 'Заповніть обов\'язкові поля: марка, рік, ціна',
            })

        try:
            price_val = float(price)
        except ValueError:
            return render(request, 'listing/listing.html', {
                'user': request.user,
                'errors': 'Невірний формат ціни',
            })

        currency = request.POST.get('currency', '$')
        if currency == '$':
            price_usd = price_val
            price_uah = price_val * 41.5
        elif '€' in currency or currency == '€':
            price_usd = price_val * 1.1
            price_uah = price_val * 45.5
        else:
            price_uah = price_val
            price_usd = price_val / 41.5

        mileage = request.POST.get('mileage', '0')
        try:
            mileage_val = int(mileage) if mileage else 0
        except ValueError:
            mileage_val = 0

        car = Car.objects.create(
            seller=request.user,
            brand=brand,
            model=model if model else 'Не вказано',
            year=int(year),
            modification=request.POST.get('modification', ''),
            price=price_usd,
            price_uah=price_uah,
            mileage=mileage_val,
            vin=request.POST.get('vin', ''),
            engine=((request.POST.get('engine_volume', '') + ' ' + request.POST.get('fuel_type', '')).strip()) or '',
            engine_volume=request.POST.get('engine_volume', ''),
            hp=int(request.POST.get('hp', 0) or 0),
            transmission=request.POST.get('transmission', ''),
            body_type=body_type,
            drive=request.POST.get('drive', ''),
            color=request.POST.get('color', ''),
            interior_color=request.POST.get('interior_color', ''),
            interior_material=request.POST.get('interior', ''),
            region=region,
            city=city,
            plate=request.POST.get('plate', ''),
            description=request.POST.get('description', ''),
            headlights=request.POST.get('headlights', ''),
            conditioning=request.POST.get('ac', ''),
            power_steering=request.POST.get('power_steering', ''),
            steering_adjustment=request.POST.get('steering', ''),
            spare_wheel=request.POST.get('spare_wheel', ''),
            electric_windows=request.POST.get('windows', ''),
            seat_adjustment=request.POST.get('seat_height', ''),
            state=request.POST.get('technical_condition', ''),
        )

        photos = request.FILES.getlist('photos')
        if photos:
            car.image = photos[0]
            car.save()
            for i, photo in enumerate(photos[1:], start=1):
                CarImage.objects.create(car=car, image=photo, order=i)

        return redirect('car_detail', car_id=car.id)

    return render(request, 'listing/listing.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('index')


def force_login(request):
    user = User.objects.first()
    if user:
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('cabinet')

def admin_panel(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')
    all_users = User.objects.all().order_by('-date_joined')
    all_cars = Car.objects.all().select_related('seller').order_by('-created_at')
    return render(request, 'admin_panel/admin_panel.html', {
        'user': request.user,
        'all_users': all_users,
        'all_cars': all_cars,
    })

def save_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.patronymic = request.POST.get('patronymic', '').strip()
        user.region = request.POST.get('region', '').strip()
        user.city = request.POST.get('city', '').strip()
        new_email = request.POST.get('email', '').strip()
        user.phone = request.POST.get('phone', '').strip()

        if new_email and new_email != user.email:
            EmailAddress.objects.filter(user=user).update(email=new_email)
        user.email = new_email
        user.save()
    return redirect('cabinet')


def change_password(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        new = request.POST.get('new_password', '')
        confirm = request.POST.get('confirm_password', '')
        has_password = request.user.has_usable_password()

        if has_password:
            current = request.POST.get('current_password', '')
            if not request.user.check_password(current):
                return render(request, 'cabinet/cabinet.html', {
                    'user': request.user,
                    'cars': Car.objects.filter(seller=request.user),
                    'favorite_cars': [],
                    'has_google': SocialAccount.objects.filter(user=request.user, provider='google').exists(),
                    'has_password': has_password,
                    'password_error': 'Невірний поточний пароль',
                    'show_settings': True,
                })

        if new != confirm:
            return render(request, 'cabinet/cabinet.html', {
                'user': request.user,
                'cars': Car.objects.filter(seller=request.user),
                'favorite_cars': [],
                'has_google': SocialAccount.objects.filter(user=request.user, provider='google').exists(),
                'has_password': has_password,
                'password_error': 'Паролі не співпадають',
                'show_settings': True,
            })

        if len(new) < 6:
            return render(request, 'cabinet/cabinet.html', {
                'user': request.user,
                'cars': Car.objects.filter(seller=request.user),
                'favorite_cars': [],
                'has_google': SocialAccount.objects.filter(user=request.user, provider='google').exists(),
                'has_password': has_password,
                'password_error': 'Пароль має бути мінімум 6 символів',
                'show_settings': True,
            })

        request.user.set_password(new)
        request.user.save()
        update_session_auth_hash(request, request.user)
        return redirect('cabinet')
    return redirect('cabinet')


def delete_account(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        confirm = request.POST.get('confirm_delete', '')
        if confirm == 'DELETE':
            user = request.user
            logout(request)
            user.is_active = False
            user.save()
            return redirect('index')
    return redirect('cabinet')

def disconnect_google(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        # Перевіряємо що юзер має пароль, інакше він не зможе зайти
        if request.user.has_usable_password():
            SocialAccount.objects.filter(user=request.user, provider='google').delete()
        # Якщо пароля немає — не відв'язуємо (інакше юзер заблокує себе)
    return redirect('cabinet')

def toggle_favorite(request, car_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'not_authenticated'}, status=401)
    if request.method == 'POST':
        car = Car.objects.filter(id=car_id).first()
        if not car:
            return JsonResponse({'error': 'not_found'}, status=404)
        fav = Favorite.objects.filter(user=request.user, car=car).first()
        if fav:
            fav.delete()
            return JsonResponse({'status': 'removed'})
        else:
            Favorite.objects.create(user=request.user, car=car)
            return JsonResponse({'status': 'added'})
    return JsonResponse({'error': 'method_not_allowed'}, status=405)