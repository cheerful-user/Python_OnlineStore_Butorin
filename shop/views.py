from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .models import Product, Order, OrderItem, OrderStatus, Client
from .forms import CartAddForm
from .utils import Cart
from users.forms import CustomUserCreationForm, ClientProfileForm


@login_required
def profile(request):
    """Личный кабинет с историей заказов"""
    client = request.user.client
    orders = client.orders.all().order_by('-created_at')
    return render(request, 'shop/profile.html', {'client': client, 'orders': orders})


def product_list(request):
    """Отображает список всех товаров."""
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override_quantity']
        )
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart_detail.html', {'cart': cart})


def home(request):
    """Главная страница с логином и регистрацией"""
    register_user_form = CustomUserCreationForm(request.POST or None)
    register_client_form = ClientProfileForm(request.POST or None)
    login_form = AuthenticationForm(request, request.POST or None)

    if request.method == 'POST':
        if 'register_submit' in request.POST:
            if register_user_form.is_valid() and register_client_form.is_valid():
                user = register_user_form.save()
                Client.objects.create(user=user, **register_client_form.cleaned_data)
                auth_login(request, user)
                messages.success(request, 'Регистрация прошла успешно! Добро пожаловать.')
                return redirect('home')

        elif 'login_submit' in request.POST:
            if login_form.is_valid():
                auth_login(request, login_form.get_user())
                return redirect('product_list')

    return render(request, 'shop/home.html', {
        'register_user_form': register_user_form,
        'register_client_form': register_client_form,
        'login_form': login_form,
    })


def order_create(request):
    """
    Единая точка входа для оформления заказа.
    Разделяет логику для гостей и авторизованных пользователей.
    """
    cart = Cart(request)

    # Если корзина пуста, нет смысла показывать страницу
    if len(cart) == 0:
        return redirect('product_list')

    # --- ЛОГИКА ДЛЯ ГОСТЕЙ (не авторизован) ---
    if not request.user.is_authenticated:
        register_user_form = CustomUserCreationForm(request.POST or None)
        register_client_form = ClientProfileForm(request.POST or None)
        login_form = AuthenticationForm(request, request.POST or None)

        if request.method == 'POST':
            if 'register_submit' in request.POST:
                if register_user_form.is_valid() and register_client_form.is_valid():
                    user = register_user_form.save()
                    Client.objects.create(user=user, **register_client_form.cleaned_data)
                    auth_login(request, user)
                    messages.success(request, 'Вы успешно зарегистрировались!')
                    return _


            elif 'login_submit' in request.POST:
                if login_form.is_valid():
                    user = login_form.get_user()
                    auth_login(request, user)
                    return _process_order(request, cart, user.client)

        # Если это GET-запрос или POST с ошибками валидации
        return render(request, 'shop/order_create.html', {
            'cart': cart,
            'register_user_form': register_user_form,
            'register_client_form': register_client_form,
            'login_form': login_form,
        })

    # --- ЛОГИКА ДЛЯ АВТОРИЗОВАННЫХ ПОЛЬЗОВАТЕЛЕЙ ---
    else:
        # Пользователь уже вошел в систему. Сразу получаем его клиента.
        client = request.user.client
        return _process_order(request, cart, client)


def _process_order(request, cart, client):
    """
    Основная логика создания заказа.
    Вызывается как для гостей после их регистрации, так и для авторизованных пользователей.
    """
    # Создаем заказ
    order = Order.objects.create(
        client=client,
        status=OrderStatus.objects.get(name='Новый')
    )

    # Создаем товары в заказе из корзины
    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            quantity=item['quantity'],
            unit_price_at_purchase=item['product'].price
        )

    # Очищаем корзину после успешного оформления
    cart.clear()

    # Показываем страницу успешного заказа
    return render(request, 'shop/order_created.html', {'order': order})


@login_required
def order_detail(request, order_id):
    """
    Просмотр деталей конкретного заказа.
    """
    # Получаем заказ, проверяя, что он принадлежит текущему пользователю
    order = get_object_or_404(Order, id=order_id, client__user=request.user)

    # ПОДГОТОВКА ДАННЫХ: Используем 'items' вместо 'orderitem_set'
    items_with_total = []
    for item in order.items.all():  # <-- ИЗМЕНЕНИЕ ЗДЕСЬ
        item.total_price = item.quantity * item.unit_price_at_purchase
        items_with_total.append(item)

    return render(request, 'shop/order_detail.html', {
        'order': order,
        'items': items_with_total,
    })