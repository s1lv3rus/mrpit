from django.shortcuts import render, redirect
from orders.models import Order
from yandex_checkout import Payment, Configuration, WebhookNotification
from datetime import datetime
from shop.views import list
import json
from django.http import HttpResponse


def payment_process(*args, order_id):
    Configuration.account_id = '681662'
    Configuration.secret_key = 'test_u651SuGAV4prh_qhRk7OE1DvaboIciuK48ixpS7MBzg'
    order = Order.published.get(id=order_id)
    value = float(order.get_total_cost() + order.deliver_cost)
    description = order.id

    payment = Payment.create({
        "amount": {
            "value": value,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "http://127.0.0.1:8000"
        },
        "description": description
    })

    return redirect(payment.confirmation.confirmation_url)


def notifications(request):
    event_json = json.loads(request.body)
    try:
        notification_object = WebhookNotification(event_json)
    except Exception:
        notification_object = None
    payment = notification_object.object
    order = Order.published.get(id=payment.description)
    # order.paid = True
    # order.save()
    return HttpResponse(status=200)


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
