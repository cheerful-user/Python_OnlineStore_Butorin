# shop/forms.py

from django import forms
from .models import Client


class CartAddForm(forms.Form):
    product = forms.IntegerField(widget=forms.HiddenInput)
    quantity = forms.IntegerField(min_value=1, max_value=10, initial=1,
                                  widget=forms.NumberInput(attrs={'style': 'width: 50px;'}))
    override_quantity = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


# --- ФОРМА ДЛЯ ЗАКАЗА ---
class OrderForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['last_name', 'first_name', 'email', 'address_line_1']

        labels = {
            'address_line_1': 'Адрес (улица, дом)',
        }