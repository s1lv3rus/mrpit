from django import forms
from shop.models import *

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]



class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label='Количество')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class GiftForm(forms.Form):
    gift = forms.Field()
