from django.shortcuts import render, redirect

from yandex_checkout import Payment, Configuration, WebhookNotification

import json

json1 = """
{
  "type": "notification",
  "event": "payment.succeeded",
  "object": {
    "id": "260be206-000f-5000-a000-1db8f6dfd804",
    "status": "succeeded",
    "paid": true,
    "amount": {
      "value": "2938.00",
      "currency": "RUB"
    },
    "authorization_details": {
      "rrn": "342400225654",
      "auth_code": "224762"
    },
    "captured_at": "2020-03-24T09:09:40.003Z",
    "created_at": "2020-03-24T09:09:26.414Z",
    "description": "22",
    "metadata": {},
    "payment_method": {
      "type": "bank_card",
      "id": "260be206-000f-5000-a000-1db8f6dfd804",
      "saved": false,
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
    "refundable": true,
    "refunded_amount": {
      "value": "0.00",
      "currency": "RUB"
    },
    "test": true
  }
}
"""
with open('package.json', 'r') as f:
    event_json = json.loads(f.read())
# event_json = json.loads(json1)
    description = int(event_json["object"]["description"])
# order = Order.published.get(id=value)
# order.paid = True
# order.save()
print(description)
