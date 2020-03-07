from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import *
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm


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
    products_rec = Product.published.filter(recommendation=True)
    suppliers = Supplier.published.all()
    objectives = Objective.published.all()
    offers = Offer.published.all()
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'update': True})
    coupon_apply_form = CouponApplyForm()
    template = 'cart/detail.html'
    context = locals()
    return render(request, template, context)
