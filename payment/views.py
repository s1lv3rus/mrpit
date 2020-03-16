from django.shortcuts import render, redirect
from orders.models import Order
from .forms import PaymentCreateForm
from datetime import datetime
from shop.views import list
import base64
import hashlib


def get_raw_signature(params):
    chunks = []

    for key in sorted(params.keys()):
        if key == 'signature':
            continue

        value = params[key]

        if isinstance(value, str):
            value = value.encode('utf8')
        else:
            value = str(value).encode('utf-8')

        if not value:
            continue

        value_encoded = base64.b64encode(value)
        chunks.append('%s=%s' % (key, value_encoded.decode()))

    raw_signature = '&'.join(chunks)
    return raw_signature


'''Двойное шифрование sha1 на основе секретного ключа'''


def double_sha1(secret_key, data):
    sha1_hex = lambda s: hashlib.sha1(s.encode('utf-8')).hexdigest()
    digest = sha1_hex(secret_key + sha1_hex(secret_key + data))
    return digest


'''Вычисляем подпись (signature). Подпись считается на основе склеенной строки из отсортированного массива 
параметров, исключая из расчета пустые поля и элемент "signature" '''


def get_signature(secret_key: str, params: dict) -> str:
    return double_sha1(secret_key, get_raw_signature(params))


'''Определяем словарь с параметрами для расчета. В этот массив должны войти все параметры, отправляемые в вашей форме 
(за исключением самого поля signature, значение которого вычисляем). Получив вашу форму, система ИЭ аналогичным 
образом вычислит из ее параметров signature и сравнит значение с вычисленным на стороне вашего магазина. подставьте 
ваш секретный ключ вместо 00112233445566778899aabbccddeeff '''


def payment_process(request, order_id):
    [categories, suppliers, objectives, products_rec, offers] = list()
    order = Order.published.get(id=order_id)
    amount = float(order.get_total_cost())
    merchant = '29058e72-9aef-4ebf-8931-e9f4bac69b13'
    unix_timestamp = '1573451160'

    form = PaymentCreateForm(request.POST)
    template = 'payment/process.html'
    items = {
        "testing": '1',
        "salt": 'dPUTLtbMfcTGzkaBnGtseKlcQymCLrYI',
        "order_id": order.id,
        "amount": amount,
        "merchant": '29058e72-9aef-4ebf-8931-e9f4bac69b13',
        "description": 'Заказ c магазина https://mrpit.online',
        "success_url": 'https://mrpit.online',
        "receipt_contact": 'admin@mrpit.online',
        "unix_timestamp": '1573451160'
    }
    signature = get_signature('CF71A321C48FDE4CB5EFE141CD5DC1AF', items)
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
