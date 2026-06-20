from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Car, CarImage, Favorite


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_verified_seller', 'rating', 'is_staff')
    list_filter = ('is_verified_seller', 'is_staff', 'is_superuser', 'is_active')

    fieldsets = UserAdmin.fieldsets + (
        ('Додатково', {
            'fields': ('phone', 'patronymic', 'region', 'city',
                       'rating', 'balance', 'avatar',
                       'is_verified_seller', 'years_on_site', 'last_online')
        }),
    )


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'price', 'city',
                    'seller', 'is_active', 'created_at')
    list_filter = ('is_active', 'brand', 'transmission', 'body_type')
    search_fields = ('brand', 'model', 'vin', 'plate')
    inlines = [CarImageInline]


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'created_at')