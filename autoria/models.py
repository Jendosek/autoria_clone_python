# autoria/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from autoria.storage import CloudinaryStorage


class User(AbstractUser):
    phone = models.CharField('Телефон', max_length=20, blank=True)
    patronymic = models.CharField('По батькові', max_length=100, blank=True)
    region = models.CharField('Область', max_length=100, blank=True)
    city = models.CharField('Місто', max_length=100, blank=True)
    rating = models.IntegerField('Рейтинг', default=25)
    balance = models.DecimalField('Баланс', max_digits=10, decimal_places=2, default=0)
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True,
                               storage=CloudinaryStorage(folder='avatars'))

    # Поля продавця
    is_verified_seller = models.BooleanField('Верифікований продавець', default=False)
    years_on_site = models.CharField('Років на сайті', max_length=20, blank=True)
    last_online = models.DateTimeField('Останній раз онлайн', null=True, blank=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'.strip() or self.username


class Car(models.Model):
    """Оголошення автомобіля"""
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='cars', verbose_name='Продавець'
    )

    # Основне
    brand = models.CharField('Марка', max_length=100)
    model = models.CharField('Модель', max_length=100)
    year = models.IntegerField('Рік')
    generation = models.CharField('Покоління', max_length=100, blank=True)
    modification = models.CharField('Модифікація', max_length=100, blank=True)

    # Ціна
    price = models.DecimalField('Ціна USD', max_digits=12, decimal_places=2)
    price_uah = models.DecimalField('Ціна UAH', max_digits=12, decimal_places=2)
    old_price = models.DecimalField('Стара ціна', max_digits=12, decimal_places=2,
                                     null=True, blank=True)
    credit_monthly = models.DecimalField('Кредит/міс', max_digits=10, decimal_places=2,
                                          null=True, blank=True)

    # Технічне
    mileage = models.IntegerField('Пробіг (тис. км)')
    engine = models.CharField('Двигун', max_length=100)
    engine_volume = models.CharField("Об'єм двигуна", max_length=20, blank=True)
    hp = models.IntegerField('К.с.', null=True, blank=True)
    transmission = models.CharField('КПП', max_length=50)
    body_type = models.CharField('Тип кузова', max_length=50, blank=True)
    doors = models.IntegerField('Двері', default=4)
    seats = models.IntegerField('Місця', default=5)
    drive = models.CharField('Привід', max_length=50, blank=True)
    eco_standard = models.CharField('Екостандарт', max_length=50, blank=True)

    # Витрата палива
    fuel_city = models.FloatField('Витрата місто', null=True, blank=True)
    fuel_highway = models.FloatField('Витрата траса', null=True, blank=True)
    fuel_mixed = models.FloatField('Витрата змішаний', null=True, blank=True)

    # Зовнішність / салон
    color = models.CharField('Колір', max_length=50, blank=True)
    color_hex = models.CharField('Колір HEX', max_length=7, blank=True)
    interior_color = models.CharField('Колір салону', max_length=50, blank=True)
    interior_material = models.CharField('Матеріал салону', max_length=50, blank=True)

    # Локація
    city = models.CharField('Місто', max_length=100)
    region = models.CharField('Область', max_length=100, blank=True)
    zip_code = models.CharField('Індекс', max_length=10, blank=True)

    # Ідентифікація
    vin = models.CharField('VIN', max_length=17, blank=True)
    plate = models.CharField('Держномер', max_length=20, blank=True)

    # Контент
    description = models.TextField('Опис', blank=True)
    image = models.ImageField('Головне фото', upload_to='cars/', blank=True,
                              storage=CloudinaryStorage(folder='cars'))

    # Стан
    owners = models.IntegerField('Власників', default=1)
    state = models.CharField('Стан', max_length=200, blank=True)

    # Обладнання
    safety = models.TextField('Безпека', blank=True)
    comfort = models.TextField('Комфорт', blank=True)
    multimedia = models.TextField('Мультимедіа', blank=True)
    headlights = models.CharField('Фари', max_length=100, blank=True)
    conditioning = models.CharField('Кондиціонер', max_length=100, blank=True)
    power_steering = models.CharField('Підсилювач керма', max_length=50, blank=True)
    steering_adjustment = models.CharField('Регулювання керма', max_length=100, blank=True)
    spare_wheel = models.CharField('Запасне колесо', max_length=50, blank=True)
    optics = models.TextField('Оптика', blank=True)
    parking_help = models.TextField('Допомога при паркуванні', blank=True)
    airbags = models.TextField('Подушки безпеки', blank=True)
    electric_windows = models.CharField('Електросклопідйомники', max_length=100, blank=True)
    seat_adjustment = models.CharField('Регулювання сидінь', max_length=200, blank=True)

    # Теги (зберігаємо як JSON список)
    tags = models.JSONField('Теги', default=list, blank=True)

    # Статус
    is_active = models.BooleanField('Активне', default=True)
    created_at = models.DateTimeField('Створено', auto_now_add=True)
    updated_at = models.DateTimeField('Оновлено', auto_now=True)

    @property
    def seller_name(self):
        return self.seller.first_name or self.seller.username

    @property
    def seller_verified(self):
        return self.seller.is_verified_seller

    @property
    def seller_years(self):
        return self.seller.years_on_site

    @property
    def seller_phone(self):
        return self.seller.phone

    @property
    def seller_online(self):
        if self.seller.last_online:
            return f"Був в мережі {self.seller.last_online.strftime('%d.%m.%Y о %H:%M')}"
        return ''

    @property
    def posted(self):
        from django.utils import timezone
        from django.utils.timesince import timesince
        return f"{timesince(self.created_at, timezone.now())} тому"

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        # Fallback на дефолтну картинку
        return '/static/images/index/filter_logos/default_logo.png'

    class Meta:
        db_table = 'cars'
        ordering = ['-created_at']
        verbose_name = 'Автомобіль'
        verbose_name_plural = 'Автомобілі'

    def __str__(self):
        return f'{self.brand} {self.model} {self.year}'


class CarImage(models.Model):
    """Додаткові фото для галереї"""
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE,
        related_name='images', verbose_name='Автомобіль'
    )
    image = models.ImageField('Фото', upload_to='cars/gallery/',
                              storage=CloudinaryStorage(folder='cars/gallery'))
    is_main = models.BooleanField('Головне', default=False)
    order = models.IntegerField('Порядок', default=0)

    class Meta:
        db_table = 'car_images'
        ordering = ['order']
        verbose_name = 'Фото автомобіля'
        verbose_name_plural = 'Фото автомобілів'

    def __str__(self):
        return f'Фото {self.order} — {self.car}'


class Favorite(models.Model):
    """Обране: юзер зберігає машину"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorites', verbose_name='Користувач'
    )
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE,
        related_name='favorited_by', verbose_name='Автомобіль'
    )
    created_at = models.DateTimeField('Додано', auto_now_add=True)

    class Meta:
        db_table = 'favorites'
        unique_together = ('user', 'car')
        verbose_name = 'Обране'
        verbose_name_plural = 'Обране'

    def __str__(self):
        return f'{self.user} → {self.car}'