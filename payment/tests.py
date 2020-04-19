import requests
from django.shortcuts import render, redirect

from yandex_checkout import Payment, Configuration, WebhookNotification

import json

json1 = {
  "type": "notification",
  "event": "payment.succeeded",
  "object": {
    "id": "26115c13-000f-5000-9000-1ad291d11fb8",
    "status": "succeeded",
    "paid": 'true',
    "amount": {
      "value": "1300.00",
      "currency": "RUB"
    },
    "authorization_details": {
      "rrn": "175228456294",
      "auth_code": "455262"
    },
    "captured_at": "2020-03-28T12:51:45.765Z",
    "created_at": "2020-03-28T12:51:31.379Z",
    "description": "80",
    "metadata": {},
    "payment_method": {
      "type": "bank_card",
      "id": "26115c13-000f-5000-9000-1ad291d11fb8",
      "saved": 'false',
      "card": {
        "first6": "555555",
        "last4": "4444",
        "expiry_month": "12",
        "expiry_year": "2020",
        "card_type": "MasterCard",
        "issuer_country": "US"
      },
      "title": "Bank card *4444"
    },
    "recipient": {
      "account_id": "681662",
      "gateway_id": "1687646"
    },
    "refundable": 'true',
    "refunded_amount": {
      "value": "0.00",
      "currency": "RUB"
    },
    "test": 'true'
  }
}

host = "http://127.0.0.1:8000"
path = "/payment/notifications/"
url = host + path

request_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json;charset=UTF-8"
}

response = requests.post(url, headers=request_headers, data=json.dumps(json1))
description = response.status_code
# event_json = json.loads(response.text)
# description = int(event_json["object"]['description'])
# order = Order.published.get(id=description)
# order.paid = True
# order.save()
print(description)
