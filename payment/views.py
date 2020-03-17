from django.shortcuts import render, redirect
from orders.models import Order
from yandex_checkout import Payment, Configuration
from datetime import datetime
from shop.views import list


def payment_process(request, order_id):
    order = Order.published.get(id=order_id)
    Configuration.account_id = '681662'
    Configuration.secret_key = 'test_u651SuGAV4prh_qhRk7OE1DvaboIciuK48ixpS7MBzg'

    order = Order.published.get(id=order_id)
    value = float(order.get_total_cost())

    payment = Payment.create({
        "amount": {
            "value": value,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://mrpit.online"
        },
        "description": "Заказ №1"
    })

    return redirect(payment.confirmation.confirmation_url)


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
