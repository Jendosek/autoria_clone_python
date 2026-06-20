"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', views.index, name='index'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('login/', views.login_view, name='login'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('add/', views.add_listing, name='add_listing'),
    path('logout/', views.logout_view, name='logout'),
    path('force-login/', views.force_login, name='force_login'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    # API
    path('api/admin/users/<int:user_id>/delete/', api.api_delete_user, name='api_delete_user'),
    path('api/admin/users/<int:user_id>/unban/', api.api_unban_user, name='api_unban_user'),
    path('api/admin/cars/<int:car_id>/delete/', api.api_delete_car, name='api_delete_car'),
    path('api/admin/cars/<int:car_id>/toggle/', api.api_toggle_car, name='api_toggle_car'),
    path('cabinet/google/disconnect/', views.disconnect_google, name='disconnect_google'),

    path('cabinet/profile/save/', views.save_profile, name='save_profile'),
    path('cabinet/password/change/', views.change_password, name='change_password'),
    path('cabinet/delete/', views.delete_account, name='delete_account'),
    path('api/favorite/toggle/<int:car_id>/', views.toggle_favorite, name='toggle_favorite'),
]