import datetime


from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, redirect
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from orders.models import Order, OrderItem
from yandex_checkout import Payment, Configuration

from shop.models import Flavour

import json
import requests
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
            # Отправляем письмо администрации об оплате заказа
            subject_pay = 'Заказ №{} оплачен!'.format(order.id)
            mail_from = 'no-reply@mrpit.online'
            mail_to = ['admin@mrpit.online', 'nukez@inbox.ru']
            admin_message = 'Заказ №{} оплачен!<br>'\
                'Перейти в админку по <a href="https://mrpit.online/admin/orders/order">ссылке</a>'.format(order.id)
            mail = EmailMessage(subject_pay, admin_message, mail_from, mail_to)
            mail.content_subtype = "html"
            mail.send()

            for item in order.items.all():
                flavour = Flavour.published.get(id=item.flavour.id)
                if flavour.quantity > 0:
                    flavour.quantity -= item.quantity
                    if flavour.quantity == 0:
                        flavour.for_offer = False
                        # Отправка письма администрации о том, что товар из набора кончился и нужно формировать новый
                        subject = 'Закончился вкус у товара из набора'
                        sender = 'no-reply@mrpit.online'
                        message = 'Закончился вкус у товара из набора. {} {}\n' \
                                  'Необходимо проверить набор и при необходимости переформировать' \
                            .format(flavour.name, flavour.product.name)
                        send_mail(subject, message, sender, ['admin@mrpit.online'])
                else:
                    flavour.quantity = 0

                flavour.save()
                # Если доставка в регионы, то создаём отправление в лк почты россии
            if order.city != 'Пермь':
                russian_post_create_delivery(order_id)
            return HttpResponse(status=200)
        elif event_json["event"] == "payment.waiting_for_capture":
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=500)


def russian_post_create_delivery(order_id):
    order = Order.published.get(id=order_id)

    protocol = "https://"
    host = "otpravka-api.pochta.ru"
    token = "5SHr_TxD2ZtxgxrlN6HI7Da_Jn4ajc5Y"
    key = "am9obl9rQGluYm94LnJ1OkdnNTU1NTU2"

    request_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json;charset=UTF-8",
        "Authorization": "AccessToken " + token,
        "X-User-Authorization": "Basic " + key
    }

    path = "/1.0/user/backlog"

    new_orders = [{
        "postoffice-code": "614961",
        "tel-address": order.phone,
        "surname": order.last_name,
        "given-name": order.first_name,
        "mail-direct": 643,
        "address-type-to": "DEFAULT",
        "index-to": order.postal_code,
        "region-to": "Заполнить регион!",
        "place-to": order.city,
        "street-to": order.address,
        "house-to": "Заполнить номер дома и кв!",
        "mass": 2000,
        "mail-category": "ORDINARY",
        "mail-type": "ONLINE_PARCEL",
        "order-num": order.id
    }]

    url = protocol + host + path

    response = requests.put(
        url, headers=request_headers, data=json.dumps(new_orders)
    )

    # with open('russian_post_delivery_log.txt', 'a') as outFile:
    #     outFile.write('\nВремя отправки:{}, Код: {} Текст: {}'
    #                   .format(datetime.datetime.now(), response.status_code, response.text))
