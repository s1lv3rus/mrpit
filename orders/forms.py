from django import forms
from django.http import request

from .models import Order, OrderItem


class OrderCreateForm(forms.ModelForm):
    first_name = forms.Field(label='Имя')
    last_name = forms.Field(label='Фамилия')
    email = forms.Field(label='Email', required=False)
    city = forms.Field(label='Населенный пункт')
    address = forms.Field(label='Адрес')
    postal_code = forms.Field(label='Почтовый индекс')
    comment = forms.Field(label='Комментарий', required=False)

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'city', 'address', 'postal_code', 'deliver', 'comment']


class PermOrderCreateForm(forms.ModelForm):
    first_name = forms.Field(label='Имя')
    last_name = forms.Field(label='Фамилия')
    email = forms.EmailField(label='Email', required=False)
    address = forms.Field(label='Адрес')
    comment = forms.Field(label='Комментарий', required=False)

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'comment']
