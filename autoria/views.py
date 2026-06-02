from django.shortcuts import render

# Create your views here.

CARS = [
    {
        'id': 1,
        'brand': 'Toyota',
        'model': 'Camry',
        'year': 2021,
        'price': 28500,
        'mileage': 45,
        'engine': '2.5 Бензин',
        'transmission': 'Автомат',
        'city': 'Київ',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/a/ac/2018_Toyota_Camry_%28ASV70R%29_Ascent_sedan_%282018-08-27%29_01.jpg',
        'description': 'В відмінному стані, один власник, повний сервіс у дилера.',
    },
    {
        'id': 2,
        'brand': 'BMW',
        'model': '320d',
        'year': 2019,
        'price': 23000,
        'mileage': 120,
        'engine': '2.0 Дизель',
        'transmission': 'Автомат',
        'city': 'Вінниця',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/BMW_320d_F30_%286857485681%29.jpg/960px-BMW_320d_F30_%286857485681%29.jpg',
        'description': 'M-пакет, шкіряний салон, LED фари, навігація.',
    },
    {
        'id': 3,
        'brand': 'Volkswagen',
        'model': 'Golf 8',
        'year': 2022,
        'price': 21000,
        'mileage': 30,
        'engine': '1.5 Бензин',
        'transmission': 'Механіка',
        'city': 'Львів',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/2020_Volkswagen_Golf_Style_1.5_Front.jpg/960px-2020_Volkswagen_Golf_Style_1.5_Front.jpg',
        'description': 'Як нова, гаражне зберігання, зимова гума в комплекті.',
    },
]

def index(request):
    return render(request, 'index.html', {'cars': CARS})

def car_detail(request, car_id):
    car = next((c for c in CARS if c['id'] == car_id), None)
    return render(request, 'car_detail.html', {'car': car})


def login(request):
    return render(request, 'login.html')