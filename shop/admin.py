# 1. Импортируем модуль администратора Django
from django.contrib import admin

# 2. Импортируем наши модели из текущего приложения (models.py)
from .models import Product, Inventory, Client, OrderStatus, Order, OrderItem

# --- Регистрация простых моделей ---
# Для моделей Product, Inventory и Client используем стандартную регистрацию.
# Это самый быстрый способ добавить модель в админку.

admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(Client)
admin.site.register(OrderStatus)


# --- Расширенная регистрация для сложных моделей ---
# Для моделей с внешними ключами (ForeignKey) лучше использовать
# более продвинутую регистрацию, чтобы интерфейс был удобным.

'''было 
# 3. Класс для настройки отображения модели CartItem
class CartItemAdmin(admin.ModelAdmin):
    # В списке объектов будут видны эти поля
    list_display = ('cart', 'product', 'quantity')
    # Добавим фильтр по корзинам в правой панели
    list_filter = ('cart',)

# 4. Регистрируем CartItem с нашими настройками
admin.site.register(CartItem, CartItemAdmin)

'''


# 5. Класс для настройки отображения модели OrderItem
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'unit_price_at_purchase')
    list_filter = ('order',)

admin.site.register(OrderItem, OrderItemAdmin)


# 6. Класс для настройки модели Order (Заказы)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'status', 'created_at')
    list_filter = ('status', 'created_at') # Фильтр по статусу и дате
    search_fields = ('client__last_name', 'client__first_name') # Поиск по фамилии клиента

admin.site.register(Order, OrderAdmin)

'''было 
# 7. Класс для настройки ShoppingCart (Корзина)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('client',)

admin.site.register(ShoppingCart, ShoppingCartAdmin)

'''