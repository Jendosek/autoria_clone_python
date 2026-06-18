from django.shortcuts import render, redirect

# Create your views here.

CARS = [
    {
        'id': 1,
        'brand': 'Toyota',
        'model': 'Camry',
        'year': 2021,
        'generation': 'XV70, 8 покоління',
        'modification': '2.5 AT (209 к.с.)',
        'price': 28500,
        'price_uah': 1259700,
        'old_price': 29800,
        'mileage': 45,
        'engine': '2.5 Бензин',
        'engine_volume': '2.5 л',
        'hp': 209,
        'transmission': 'Автомат',
        'body_type': 'Седан',
        'doors': 4,
        'seats': 5,
        'drive': 'Передній',
        'color': 'Білий',
        'color_hex': '#f5f5f5',
        'interior_color': 'Чорний',
        'interior_material': 'Шкіра',
        'eco_standard': 'Євро-6',
        'fuel_city': 10,
        'fuel_highway': 6,
        'fuel_mixed': 8,
        'city': 'Київ',
        'region': 'Київська обл.',
        'zip_code': '01001',
        'plate': 'АА 1234 ВВ',
        'vin': 'JTNBF1FK5MJ012345',
        'image': '/static/images/cars/toyota_camry_car.jpg',
        'description': 'В відмінному стані, один власник, повний сервіс у дилера. Можлива доставка по домовленості!',
        'posted': '3 дні тому',
        'credit_monthly': 16200,
        'owners': 1,
        'state': 'Перший власник',

        # Продавець
        'seller_name': 'Олександр',
        'seller_verified': True,
        'seller_years': '3+ років',
        'seller_phone': '(067) XXX XX XX',
        'seller_online': 'Був в мережі сьогодні о 14:35',

        # Теги
        'tags': ['Вперше на AUTO.RIA', 'Перша реєстрація', 'Доступний кредит'],

        # Обладнання
        'safety': 'ESP, ABS, Розподіл гальмівних зусиль (EBD)',
        'comfort': 'Круїз контроль, Безключовий доступ, Підігрів сидінь, Датчик дощу',
        'multimedia': 'Акустика, Apple CarPlay, Android Auto, USB, Bluetooth, Камера заднього виду',
        'headlights': 'Світлодіодні',
        'conditioning': 'Клімат-контроль 2-зонний',
        'power_steering': 'Електро',
        'steering_adjustment': 'По висоті та по вильоту',
        'spare_wheel': 'Повнорозмірне',
        'optics': 'Датчик світла, Денні ходові вогні',
        'parking_help': 'Парктронік задній, Камера заднього виду',
        'airbags': 'Водія, Пасажира, Бічні передні, Бічні задні, Віконні (шторки)',
        'electric_windows': 'Передні та задні',
        'seat_adjustment': 'Електрорегулювання сидіння водія',
    },
    {
        'id': 2,
        'brand': 'BMW',
        'model': '320d',
        'year': 2019,
        'generation': 'G20, 7 покоління',
        'modification': '2.0 AT (190 к.с.)',
        'price': 23000,
        'price_uah': 1016600,
        'old_price': None,
        'mileage': 120,
        'engine': '2.0 Дизель',
        'engine_volume': '2.0 л',
        'hp': 190,
        'transmission': 'Автомат',
        'body_type': 'Седан',
        'doors': 4,
        'seats': 5,
        'drive': 'Задній',
        'color': 'Чорний',
        'color_hex': '#1a1a1a',
        'interior_color': 'Чорний',
        'interior_material': 'Шкіра',
        'eco_standard': 'Євро-6',
        'fuel_city': 7,
        'fuel_highway': 4,
        'fuel_mixed': 5,
        'city': 'Вінниця',
        'region': 'Вінницька обл.',
        'zip_code': '21000',
        'plate': 'ВІ 5678 АН',
        'vin': 'WBA5R1C50KAK78901',
        'image': '/static/images/cars/bmw_m5_car.jpg',
        'description': 'M-пакет, шкіряний салон, LED фари, навігація. Повний сервіс у офіційного дилера BMW. Без ДТП.',
        'posted': 'Місяць тому',
        'credit_monthly': 13100,
        'owners': 2,
        'state': 'Не бита, не фарбована',

        # Продавець
        'seller_name': 'Дмитро',
        'seller_verified': True,
        'seller_years': '7+ років',
        'seller_phone': '(097) XXX XX XX',
        'seller_online': 'Був в мережі вчора о 21:10',

        # Теги
        'tags': ['Перевірений VIN', 'Не бита, не фарбована', 'Доступний кредит'],

        # Обладнання
        'safety': 'ESP, ABS, EBD, Асистент руху по смузі, Автоматичне екстрене гальмування',
        'comfort': 'Круїз контроль адаптивний, Безключовий доступ, Підігрів сидінь, Підігрів керма, Датчик дощу, Люк',
        'multimedia': 'Акустика Harman Kardon, Навігаційна система, Apple CarPlay, Android Auto, USB, Bluetooth, Бездротова зарядка',
        'headlights': 'LED адаптивні',
        'conditioning': 'Клімат-контроль 3-зонний',
        'power_steering': 'Електро',
        'steering_adjustment': 'По висоті та по вильоту',
        'spare_wheel': 'Докатка',
        'optics': 'Датчик світла, Система адаптивного освітлення, Денні ходові вогні',
        'parking_help': 'Парктронік передній та задній, Камера заднього виду 360',
        'airbags': 'Водія, Пасажира, Бічні передні, Бічні задні, Віконні (шторки), Колін водія',
        'electric_windows': 'Передні та задні',
        'seat_adjustment': 'Електрорегулювання сидіння водія та пасажира з памяттю',
    },
    {
        'id': 3,
        'brand': 'Volkswagen',
        'model': 'Golf 8',
        'year': 2022,
        'generation': 'Mk8, 8 покоління',
        'modification': '1.5 MT (150 к.с.)',
        'price': 21000,
        'price_uah': 928200,
        'old_price': 22500,
        'mileage': 30,
        'engine': '1.5 Бензин',
        'engine_volume': '1.5 л',
        'hp': 150,
        'transmission': 'Механіка',
        'body_type': 'Хетчбек',
        'doors': 5,
        'seats': 5,
        'drive': 'Передній',
        'color': 'Сірий',
        'color_hex': '#7a7a7a',
        'interior_color': 'Сірий',
        'interior_material': 'Тканина',
        'eco_standard': 'Євро-6d',
        'fuel_city': 7,
        'fuel_highway': 5,
        'fuel_mixed': 6,
        'city': 'Львів',
        'region': 'Львівська обл.',
        'zip_code': '79000',
        'plate': 'ВС 9012 КР',
        'vin': 'WVWZZZCDZMW456789',
        'image': '/static/images/cars/volkswagen_golf_car.jpeg',
        'description': 'Як нова, гаражне зберігання, зимова гума в комплекті. Пробіг оригінальний, підтверджений сервісною книжкою.',
        'posted': '18 днів тому',
        'credit_monthly': 11900,
        'owners': 1,
        'state': 'Перший власник, Перша реєстрація',

        # Продавець
        'seller_name': 'Марія',
        'seller_verified': False,
        'seller_years': '1 рік',
        'seller_phone': '(063) XXX XX XX',
        'seller_online': 'Була в мережі сьогодні о 09:15',

        # Теги
        'tags': ['Вперше на AUTO.RIA', 'Перша реєстрація', 'Гаражне зберігання'],

        # Обладнання
        'safety': 'ESP, ABS, EBD, Асистент утримання смуги',
        'comfort': 'Круїз контроль, Підігрів сидінь, Датчик дощу, Оздоблення керма шкірою',
        'multimedia': 'Акустика, Apple CarPlay, Android Auto, USB-C, Bluetooth',
        'headlights': 'Світлодіодні',
        'conditioning': 'Клімат-контроль',
        'power_steering': 'Електро',
        'steering_adjustment': 'По висоті та по вильоту',
        'spare_wheel': 'Ремкомплект',
        'optics': 'Датчик світла, Денні ходові вогні',
        'parking_help': 'Парктронік задній',
        'airbags': 'Водія, Пасажира, Бічні передні, Віконні (шторки)',
        'electric_windows': 'Передні та задні',
        'seat_adjustment': 'Механічне з регулюванням поперекового упору',
    },
]

USER = {
    'id': 17160024,
    'first_name': 'Євгеній',
    'last_name': 'Балакер',
    'phone': '+38 (068) 817 07 71',
    'email': '',
    'patronymic': '',
    'region': '',
    'city': '',
    'rating': 25,
    'balance': 0,
}


def index(request):
    return render(request, 'index/index.html', {
        'cars': CARS,
        'is_logged_in': request.session.get('is_logged_in', False),
    })


def car_detail(request, car_id):
    car = next((c for c in CARS if c['id'] == car_id), None)
    return render(request, 'car_detail/car_detail.html', {
        'car': car,
        'is_logged_in': request.session.get('is_logged_in', False),
    })


def login_view(request):
    if request.session.get('is_logged_in'):
        return redirect('cabinet')
    if request.method == 'POST':
        request.session['is_logged_in'] = True
        return redirect('cabinet')
    return render(request, 'login/login.html')


def cabinet(request):
    if not request.session.get('is_logged_in'):
        return redirect('login')
    return render(request, 'cabinet/cabinet.html', {
        'user': USER,
        'cars': CARS,
    })


def logout_view(request):
    request.session.flush()
    return redirect('index')

def force_login(request):
    request.session['is_logged_in'] = True
    return redirect('cabinet')

def add_listing(request):
    if not request.session.get('is_logged_in'):
        return redirect('login')
    return render(request, 'listing/listing.html', {'user': USER})

