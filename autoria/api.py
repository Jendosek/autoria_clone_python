from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import User, Car


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def api_delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        if user.is_superuser:
            return Response({'error': 'Не можна видалити суперадміна'}, status=403)
        user.is_active = False
        user.save()
        Car.objects.filter(seller=user).update(is_active=False)
        hidden_count = Car.objects.filter(seller=user).count()
        return Response({'status': 'banned', 'id': user_id, 'hidden_cars': hidden_count})
    except User.DoesNotExist:
        return Response({'error': 'Користувач не знайдений'}, status=404)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def api_unban_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()
        # Повертаємо оголошення розбаненого юзера
        Car.objects.filter(seller=user).update(is_active=True)
        restored_count = Car.objects.filter(seller=user).count()
        return Response({'status': 'unbanned', 'id': user_id, 'restored_cars': restored_count})
    except User.DoesNotExist:
        return Response({'error': 'Користувач не знайдений'}, status=404)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def api_delete_car(request, car_id):
    try:
        car = Car.objects.get(id=car_id)
        car.delete()
        return Response({'status': 'deleted', 'id': car_id})
    except Car.DoesNotExist:
        return Response({'error': 'Оголошення не знайдене'}, status=404)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def api_toggle_car(request, car_id):
    try:
        car = Car.objects.get(id=car_id)
        car.is_active = not car.is_active
        car.save()
        return Response({'status': 'active' if car.is_active else 'inactive', 'id': car_id})
    except Car.DoesNotExist:
        return Response({'error': 'Оголошення не знайдене'}, status=404)