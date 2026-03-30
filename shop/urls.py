# shop/urls.py

from django.urls import path
from . import views
from .views import home, cart_add, cart_detail, cart_remove


urlpatterns = [
    path('', home, name='home'), #  ГЛАВНАЯ СТРАНИЦА
    path('products/', views.product_list, name='product_list'),

    # Корзина
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', cart_remove, name='cart_remove'),

    # просмотр деталей своего заказа
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),

    # Оформление заказа
    path('order/create/', views.order_create, name='order_create'),

    path('profile/', views.profile, name='profile')
]