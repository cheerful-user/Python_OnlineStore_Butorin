from shop.models import Client
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # Или 'shop.models import Client' в зависимости от структуры


# Форма для создания пользователя (никнейм и пароль)
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)  # Только никнейм


# Форма для данных клиента (остальные поля)
class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['last_name', 'first_name', 'middle_name', 'phone_number', 'email', 'address_line_1', 'address_line_2',
                  'city', 'country']
        # Сделаем обязательные поля явно обязательными (хотя это и так в модели)
        required_fields = ['last_name', 'first_name', 'phone_number']

        labels = {
            'phone_number': 'Номер телефона',
            'address_line_1': 'Адрес (улица, дом)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.required_fields:
            self.fields[field].required = True