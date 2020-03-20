from django.shortcuts import render, redirect
from orders.models import Order
from yandex_checkout import Payment, Configuration, WebhookNotification
from datetime import datetime
from shop.views import list
import json
from django.http import HttpResponse


def payment_process(order_id):
    Configuration.account_id = '681662'
    Configuration.secret_key = 'test_u651SuGAV4prh_qhRk7OE1DvaboIciuK48ixpS7MBzg'
    order = Order.published.get(id=order_id)
    value = float(order.get_total_cost())
    description = order.id

    payment = Payment.create({
        "amount": {
            "value": value,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://mrpit.online"
        },
        "description": description
    })

    return redirect(payment.confirmation.confirmation_url)


def notifications(request):
    event_json = json.loads(request.body)
    try:
        notification_object = WebhookNotification(event_json)
        payment = notification_object.object
        description = event_json.description
        if payment.succeeded:
            order = Order.published.get(id=description)
            order.status = 'Выполнен'
            order.save()
            return payment_done(request)
        return HttpResponse(status=200)
    except Exception:
        return HttpResponse(status=500)


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
