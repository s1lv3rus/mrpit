import braintree
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order
from shop.models import *
from shop.views import list
import uuid
from yandex_checkout import Configuration, Payment, Refund
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
# import weasyprint
from io import BytesIO


def payment_process(request, order_id):
    [categories, suppliers, objectives, products_rec, offers] = list()
    order = Order.published.get(id=order_id)
    Configuration.account_id = '681662'
    Configuration.secret_key = 'test_u651SuGAV4prh_qhRk7OE1DvaboIciuK48ixpS7MBzg'

    payment = Payment.create({
        "amount": {
            "value": "2.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "embedded"
        },
        "capture": True,
        "description": "Заказ №72"
    })

    template = 'payment/process.html'
    context = locals()
    return render(request, template, context)


def payment_done(request):
    [categories, suppliers, objectives, products_rec, offers] = list()
    template = 'payment/done.html'
    context = locals()
    return render(request, template, context)


def payment_canceled(request):
    [categories, suppliers, objectives, products_rec, offers] = list()
    template = 'payment/canceled.html'
    context = locals()
    return render(request, template, context)
