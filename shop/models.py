from django.db import models
from django.contrib.auth import get_user_model

# Получаем нашу кастомную модель пользователя
User = get_user_model()


# 1. Модель Клиентов (Clients)
class Client(models.Model):
    # Связь с пользователем. Может быть пустой при регистрации.
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    # Обязательные поля (по ТЗ)
    last_name = models.CharField("Фамилия", max_length=100)
    first_name = models.CharField("Имя", max_length=100)
    phone_number = models.CharField("Номер телефона", max_length=20)

    # Необязательные поля (по ТЗ)
    middle_name = models.CharField("Отчество", max_length=100, blank=True)
    email = models.EmailField("Email", blank=True)
    address_line_1 = models.CharField("Адрес 1", max_length=255, blank=True)
    address_line_2 = models.CharField("Адрес 2", max_length=255, blank=True)
    city = models.CharField("Город", max_length=100, blank=True)
    country = models.CharField("Страна", max_length=100, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


# 2. Модель Товаров (Products)
class Product(models.Model):
    """
    Соответствует таблице 'products'.
    Каталог товаров.
    """
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    image_url = models.CharField("Ссылка на изображение", max_length=512, blank=True)

    def __str__(self):
        return self.name


# 3. Модель Запасов (Inventory)
class Inventory(models.Model):
    """
    Соответствует таблице 'inventory'.
    Связана с Products отношением 1:1.
    """
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    quantity_in_stock = models.IntegerField("Количество на складе", default=0)

    def __str__(self):
        return f"Запас для {self.product.name}"


# Вспомогательная модель для статусов заказов
class OrderStatus(models.Model):
    """
    Соответствует таблице 'order_statuses'.
    Хранит список возможных статусов заказа.
    """
    name = models.CharField("Статус", max_length=50, unique=True)  # Например: 'Новый', 'Оплачен'

    def __str__(self):
        return self.name

""" было так: 
# 4. Модель Корзины (Shopping_Carts)
class ShoppingCart(models.Model):
    
    #Соответствует таблице 'shopping_carts'.
    #Одна корзина на одного клиента.
   
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"Корзина {self.client}"



# 5. Промежуточная модель для товаров в корзине (Cart_Items)
class CartItem(models.Model):
    
    #Соответствует таблице 'cart_items'.
    #Связывает ShoppingCarts и Products.
    
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("Количество", default=1)

    class Meta:
        unique_together = ('cart', 'product')  # Одна и та же позиция не может быть добавлена дважды

"""



# 6. Модель Заказов (Orders)
class Order(models.Model):
    """
    Соответствует таблице 'orders'.
    История покупок.
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    status = models.ForeignKey(OrderStatus,
                               on_delete=models.PROTECT)  # PROTECT не даст удалить статус, если есть заказы

    # auto_now_add=True автоматически поставит текущую дату при создании
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return f"Заказ #{self.id} от {self.client}"

    def get_total_price(self):
        """Возвращает общую стоимость заказа"""
        return sum(item.quantity * item.unit_price_at_purchase for item in self.items.all())


# 7. Промежуточная модель для состава заказа (Order_Items)
class OrderItem(models.Model):
    """
    Соответствует таблице 'order_items'.
    Состав заказа.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField("Количество", default=1)

    # Сохраняем цену на момент покупки, чтобы она не менялась при обновлении каталога
    unit_price_at_purchase = models.DecimalField("Цена при покупке", max_digits=10, decimal_places=2)