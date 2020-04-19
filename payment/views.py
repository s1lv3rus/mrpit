from django.shortcuts import render, redirect
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from orders.models import Order, OrderItem
from yandex_checkout import Payment, Configuration
from datetime import datetime

from shop.models import Flavour
from shop.views import list
import json
from django.http import HttpResponse


def payment_process(*args, order_id):
    Configuration.account_id = '679610'
    Configuration.secret_key = 'live_wVEGUqZMuZd0dNd8ns_D833ejkVJs4lCD3Eu4PwgLUw'
    # Configuration.account_id = '681662'
    # Configuration.secret_key = 'test_u651SuGAV4prh_qhRk7OE1DvaboIciuK48ixpS7MBzg'
    order = Order.published.get(id=order_id)
    value = float(order.get_total_cost() + order.deliver_cost)

    json_yandex = {
        "amount": {
            "value": value,
            "currency": "RUB"
        },
        "description": 'Номер заказа: {} от {}'.format(order.id, order.created.date()),
        "metadata": {
            "order_id": order.id
        },
        "capture": True,
        "confirmation": {
            "type": "redirect",
            "return_url": "https://mrpit.online"
        },
        "receipt": {
            "customer": {
                "full_name": order.client.username,
                "email": order.email,
                "phone": order.phone
            },
            "items": [
            ]
        },
    }
    items = order.items.all()
    for item in items:
        item = {
            "description": item.flavour.product,
            "quantity": item.quantity,
            "amount": {
                "value": item.price,
                "currency": "RUB"
            },
            "vat_code": "2",
            "payment_mode": "full_prepayment",
            "payment_subject": "commodity"
        }
        json_yandex["receipt"]["items"].append(item)
    delivery_item = {
        "description": "Доставка",
        "quantity": "1",
        "amount": {
            "value": order.deliver_cost,
            "currency": "RUB"
        },
        "vat_code": "2",
        "payment_mode": "full_prepayment",
        "payment_subject": "commodity"
    }
    json_yandex["receipt"]["items"].append(delivery_item)

    payment = Payment.create(json_yandex)

    return redirect(payment.confirmation.confirmation_url)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return None


class YandexNotifications(APIView):
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        event_json = json.loads(request.body)
        if event_json["event"] == "payment.succeeded":
            order_id = int(event_json["object"]["metadata"]["order_id"])
            order = Order.published.get(id=order_id)
            order.paid = True
            order.status = "В работе"
            order.save()
            for item in order.items.all():
                flavour = Flavour.published.get(id=item.flavour.id)
                if flavour.quantity > 0:
                    flavour.quantity -= item.quantity
                    if flavour.quantity == 0:
                        flavour.for_offer = False
                else:
                    flavour.quantity = 0

                flavour.save()
            return HttpResponse(status=200)
        elif event_json["event"] == "payment.waiting_for_capture":
            return HttpResponse(status=200)
        else:
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
