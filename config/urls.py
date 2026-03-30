# config/urls.py

from django.contrib import admin
from django.urls import path, include
# Импортируем встроенные представления авторизации
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),

    # Подключаем URL-адреса приложения users (для регистрации)
    path('users/', include('users.urls')),

    # Подключаем URL-адреса приложения shop (для товаров и корзины)
    path('', include('shop.urls')),

    # --- НОВЫЕ СТРОКИ ДЛЯ АВТОРИЗАЦИИ ---

    # Встроенное представление для входа (Login)
    path('login/', auth_views.LoginView.as_view(template_name='shop/base.html'), name='login'),
    # Встроенное представление для выхода (Logout)
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),


]
