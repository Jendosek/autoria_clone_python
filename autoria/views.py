from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.db.models import Q
from .models import User, Car, Favorite, CarImage
from allauth.socialaccount.models import SocialAccount
from allauth.account.models import EmailAddress
from django.http import JsonResponse



def index(request):
    cars = Car.objects.filter(is_active=True).select_related('seller')

    # Фільтрація
    brand = request.GET.get('brand', '').strip()
    model = request.GET.getlist('model')
    year_from = request.GET.get('year_from', '')
    year_to = request.GET.get('year_to', '')
    price_from = request.GET.get('price_from', '')
    price_to = request.GET.get('price_to', '')
    regions = request.GET.getlist('region')
    fuels = request.GET.getlist('fuel')
    transmissions = request.GET.getlist('transmission')

    if brand:
        cars = cars.filter(brand__iexact=brand)
    if model:
        cars = cars.filter(model__in=model)
    if year_from:
        try:
            cars = cars.filter(year__gte=int(year_from))
        except ValueError:
            pass
    if year_to:
        try:
            cars = cars.filter(year__lte=int(year_to))
        except ValueError:
            pass
    if price_from:
        try:
            cars = cars.filter(price__gte=float(price_from))
        except ValueError:
            pass
    if price_to:
        try:
            cars = cars.filter(price__lte=float(price_to))
        except ValueError:
            pass
    if regions:
        region_map = {
            'kyiv': 'Київська', 'zhytomyr': 'Житомирська', 'sumy': 'Сумська',
            'chernihiv': 'Чернігівська', 'vinnytsia': 'Вінницька', 'poltava': 'Полтавська',
            'cherkasy': 'Черкаська', 'lviv': 'Львівська', 'ivano': 'Івано-Франківська',
            'odesa': 'Одеська', 'kherson': 'Херсонська',
        }
        region_names = [region_map.get(r, r) for r in regions]
        cars = cars.filter(region__in=region_names)
    if fuels:
        fuel_q = Q()
        for f in fuels:
            fuel_q |= Q(engine__icontains=f.replace('gasoline', 'Бензин').replace('diesel', 'Дизель').replace('gas', 'Газ').replace('electric', 'Електро').replace('hybrid', 'Гібрид'))
        cars = cars.filter(fuel_q)
    if transmissions:
        trans_map = {
            'manual': 'Механіка', 'auto': 'Автомат', 'tiptronic': 'Типтронік',
            'robot': 'Робот', 'variator': 'Варіатор',
        }
        trans_names = [trans_map.get(t, t) for t in transmissions]
        cars = cars.filter(transmission__in=trans_names)

    favorite_ids = []
    if request.user.is_authenticated:
        favorite_ids = list(Favorite.objects.filter(user=request.user).values_list('car_id', flat=True))

    has_filters = any([brand, model, year_from, year_to, price_from, price_to, regions, fuels, transmissions])

    return render(request, 'index/index.html', {
        'cars': cars,
        'is_logged_in': request.user.is_authenticated,
        'favorite_ids': favorite_ids,
        'has_filters': has_filters,
        'filter_brand': brand,
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
                if not user_obj.is_active:
                    return render(request, 'login/login.html', {
                        'error': 'Цей акаунт заблоковано. Зверніться до підтримки.'
                    })
                user = authenticate(request, username=user_obj.username, password=password)
                if user:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    # Автоматичне додавання в обране
                    next_fav = request.POST.get('next_fav') or request.GET.get('next_fav')
                    if next_fav:
                        try:
                            car = Car.objects.get(id=int(next_fav))
                            Favorite.objects.get_or_create(user=user, car=car)
                        except (Car.DoesNotExist, ValueError):
                            pass
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

            banned_by_email = User.objects.filter(email=email, is_active=False).exists()
            banned_by_phone = User.objects.filter(phone=phone, is_active=False).exists()
            if banned_by_email or banned_by_phone:
                return render(request, 'login/login.html', {
                    'reg_error': 'Реєстрація неможлива. Ці дані належать заблокованому акаунту.',
                    'show_register': True,
                })

            if User.objects.filter(email=email, is_active=True).exists():
                return render(request, 'login/login.html', {
                    'reg_error': 'Користувач з таким email вже існує',
                    'show_register': True,
                })

            if User.objects.filter(phone=phone, is_active=True).exists():
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

            next_fav = request.POST.get('next_fav') or request.GET.get('next_fav')
            if next_fav:
                try:
                    car = Car.objects.get(id=int(next_fav))
                    Favorite.objects.get_or_create(user=user, car=car)
                except (Car.DoesNotExist, ValueError):
                    pass

            return redirect('cabinet')

    return render(request, 'login/login.html', {
        'request': request,
    })


def cabinet(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_cars = Car.objects.filter(seller=request.user).select_related('seller')
    favorites = Favorite.objects.filter(user=request.user).select_related('car', 'car__seller')
    has_google = SocialAccount.objects.filter(user=request.user, provider='google').exists()

    context = {
        'user': request.user,
        'cars': user_cars,
        'favorite_cars': [fav.car for fav in favorites],
        'has_google': has_google,
        'has_password': request.user.has_usable_password(),
    }

    if request.user.is_staff:
        context['all_users'] = User.objects.all().order_by('-date_joined')
        context['all_cars'] = Car.objects.all().select_related('seller').order_by('-created_at')
        context['is_admin'] = True

    return render(request, 'cabinet/cabinet.html', context)


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
        photos = request.FILES.getlist('photos')

        errors = []
        if not brand:
            errors.append('Марка авто')
        if not model:
            errors.append('Модель авто')
        if not year:
            errors.append('Рік випуску')
        if not price:
            errors.append('Ціна')
        if not photos:
            errors.append('Фото (мінімум 1)')

        if errors:
            return render(request, 'listing/listing.html', {
                'user': request.user,
                'errors': 'Заповніть обов\'язкові поля: ' + ', '.join(errors),
            })

        try:
            price_val = float(price)
        except ValueError:
            return render(request, 'listing/listing.html', {
                'user': request.user,
                'errors': 'Невірний формат ціни',
            })

        if price_val <= 0:
            return render(request, 'listing/listing.html', {
                'user': request.user,
                'errors': 'Ціна має бути більше 0',
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

        try:
            year_val = int(year)
            if year_val < 1900 or year_val > 2026:
                return render(request, 'listing/listing.html', {
                    'user': request.user,
                    'errors': 'Невірний рік випуску',
                })
        except ValueError:
            return render(request, 'listing/listing.html', {
                'user': request.user,
                'errors': 'Невірний формат року',
            })

        # Перевірка що файли — це зображення
        for photo in photos:
            if not photo.content_type.startswith('image/'):
                return render(request, 'listing/listing.html', {
                    'user': request.user,
                    'errors': 'Дозволено завантажувати тільки зображення',
                })

        car = Car.objects.create(
            seller=request.user,
            brand=brand,
            model=model if model else 'Не вказано',
            year=year_val,
            modification=request.POST.get('modification', ''),
            price=price_usd,
            price_uah=price_uah,
            mileage=mileage_val,
            vin=request.POST.get('vin', ''),
            plate=request.POST.get('plate', ''),
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
    return redirect('cabinet')

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


BRANDS_MODELS = {
    'Audi': ['A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'Q3', 'Q5', 'Q7', 'Q8', 'e-tron', 'TT', 'RS6'],
    'BMW': ['1 Series', '2 Series', '3 Series', '5 Series', '7 Series', 'X1', 'X3', 'X5', 'X6', 'X7', 'M3', 'M5', 'iX'],
    'Chevrolet': ['Aveo', 'Bolt', 'Camaro', 'Cruze', 'Lacetti', 'Malibu', 'Spark', 'Tracker'],
    'Ford': ['Fiesta', 'Focus', 'Fusion', 'Kuga', 'Mondeo', 'Mustang', 'Puma', 'Ranger'],
    'Honda': ['Accord', 'Civic', 'CR-V', 'HR-V', 'Jazz', 'Pilot'],
    'Hyundai': ['Accent', 'Creta', 'Elantra', 'i30', 'Ioniq', 'Kona', 'Santa Fe', 'Sonata', 'Tucson'],
    'Kia': ['Ceed', 'Cerato', 'EV6', 'Niro', 'Optima', 'Rio', 'Seltos', 'Sorento', 'Sportage', 'Stinger'],
    'Mazda': ['2', '3', '6', 'CX-3', 'CX-5', 'CX-9', 'MX-5'],
    'Mercedes-Benz': ['A-Class', 'C-Class', 'E-Class', 'S-Class', 'GLA', 'GLC', 'GLE', 'GLS', 'EQS', 'V-Class'],
    'Mitsubishi': ['ASX', 'Eclipse Cross', 'L200', 'Lancer', 'Outlander', 'Pajero'],
    'Nissan': ['Juke', 'Leaf', 'Micra', 'Note', 'Qashqai', 'Rogue', 'X-Trail'],
    'Opel': ['Astra', 'Corsa', 'Crossland', 'Grandland', 'Insignia', 'Mokka', 'Zafira'],
    'Peugeot': ['2008', '208', '3008', '308', '5008', '508'],
    'Renault': ['Arkana', 'Captur', 'Clio', 'Duster', 'Kadjar', 'Koleos', 'Logan', 'Megane', 'Sandero', 'Scenic'],
    'Skoda': ['Citigo', 'Enyaq', 'Fabia', 'Kamiq', 'Karoq', 'Kodiaq', 'Octavia', 'Rapid', 'Superb'],
    'Toyota': ['Auris', 'Avensis', 'C-HR', 'Camry', 'Corolla', 'Highlander', 'Land Cruiser', 'Prius', 'RAV4', 'Supra', 'Yaris'],
    'Volkswagen': ['Arteon', 'Caddy', 'Golf', 'ID.3', 'ID.4', 'Jetta', 'Passat', 'Polo', 'T-Roc', 'Tiguan', 'Touareg'],
}

def api_brands(request):
    return JsonResponse({'brands': sorted(BRANDS_MODELS.keys())})

def api_models(request, brand):
    models = BRANDS_MODELS.get(brand, [])
    return JsonResponse({'models': models, 'brand': brand})