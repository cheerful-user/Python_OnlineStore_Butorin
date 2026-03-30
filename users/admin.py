from django.contrib import admin
from django.contrib.auth.admin import UserAdmin # Импортируем стандартный класс для управления пользователями
from .models import User # Импортируем нашу модель

# Регистрируем нашу модель User, используя стандартный интерфейс UserAdmin
admin.site.register(User, UserAdmin)