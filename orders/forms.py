from django import forms
from django.http import request

from .models import Order, OrderItem


class OrderCreateForm(forms.ModelForm):
    first_name = forms.Field(label='Имя')
    last_name = forms.Field(label='Фамилия')
    email = forms.Field(label='Email для отправки чека')
    city = forms.Field(label='Населенный пункт')
    address = forms.Field(label='Адрес')
    postal_code = forms.Field(label='Почтовый индекс')
    comment = forms.Field(label='Комментарий', required=False)

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'city', 'address', 'postal_code', 'phone', 'comment']


class PermOrderCreateForm(forms.ModelForm):
    first_name = forms.Field(label='Имя')
    last_name = forms.Field(label='Фамилия')
    email = forms.EmailField(label='Email для отправки чека')
    address = forms.Field(label='Адрес')
    comment = forms.Field(label='Комментарий', required=False)

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'phone', 'comment']


class IndexForm(forms.Form):
    postal_code = forms.IntegerField(label="Введите свой индекс")


class TrackForm(forms.Form):
    track_number = forms.Field(label="Номер отслеживания")