from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from shop.models import *
from orders.models import Order
from .cart import Cart
from .forms import CartAddProductForm, GiftForm
from coupons.forms import CouponApplyForm
import requests


# Можно поменять редирект на карточку товара снова
@require_POST
def cart_add(request, flavour_id):
    cart = Cart(request)
    flavour = Flavour.published.get(id=flavour_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(flavour=flavour,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


@require_POST
def cart_offer_add(request, flavour_id):
    cart = Cart(request)
    flavour = Flavour.published.get(id=flavour_id)
    cart.add(flavour=flavour)
    return cart


def add_offer(request, offer_id):
    products = Offer.published.get(id=offer_id).products.all()
    for product in products:
        flavour_id = product.flavour_by_product()
        cart_offer_add(request, flavour_id)
    cart = Cart(request)
    return redirect('cart:cart_detail')


def cart_remove(request, flavour_id):
    cart = Cart(request)
    flavour = Flavour.published.get(id=flavour_id)
    cart.remove(flavour)
    return redirect('cart:cart_detail')


def cart_detail(request):
    categories = Category.published.all()
    suppliers = Supplier.published.all()
    objectives = Objective.published.all()
    products_rec = Product.published.filter(recommendation=True)
    offers = Offer.published.all()
    cart = Cart(request)
    try:
        orders = Order.published.filter(client=request.user, paid=False)
    except:
        orders = None
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'update': True})

    coupon_apply_form = CouponApplyForm()
    gift_form = GiftForm()
    list_of_gift = Product.published.filter(available=False)
    gift = None
    sum_for_gift = cart.get_total_price()
    balance = 2500 - sum_for_gift
    balance2 = 5000 - sum_for_gift
    if 2500 <= sum_for_gift <= 5000:
        gift = 2500
    elif sum_for_gift > 5000:
        gift = 5000
    # Проверяем находится ли подарок в корзине перебором
    gift_in_cart = False
    for item in cart:
        flavour = item['flavour']
        # Если недоступный товар в корзине, значит подарок уже добавили
        if flavour.product.available == False:
            gift_in_cart = True
    template = 'cart/detail.html'
    context = locals()
    return render(request, template, context)


@require_POST
def add_gift(request):
    cart = Cart(request)
    gift_form = GiftForm(request.POST)
    product = None
    if gift_form.is_valid():
        gift = gift_form.cleaned_data['gift']
        if gift == 'Батончик':
            product = Product.published.get(name='Батончик(подарок)')
        elif gift == 'Шейкер 3в1':
            product = Product.published.get(name='Шейкер(подарок)')
        elif gift == 'Печенье':
            product = Product.published.get(name='Печенье(подарок)')
        try:
            flavour = product.flavour_for_gift()
            cart.add(flavour=flavour, quantity=1)
        except:
            if gift == 'Батончик+печенье':
                products = Product.published.filter(name__in=('Батончик(подарок)', 'Печенье(подарок)'))
                for product in products:
                    flavour = product.flavour_for_gift()
                    cart.add(flavour=flavour, quantity=1)
    return redirect('cart:cart_detail')
