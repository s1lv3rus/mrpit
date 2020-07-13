from django.core.mail import send_mail, EmailMessage
from django.urls import reverse
from django.shortcuts import render, redirect

from Myshop.settings import RUSSIAN_POST_TOKEN, RUSSIAN_POST_KEY
from .models import OrderItem, Order
from .forms import *
from cart.cart import Cart
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from account.models import Profile
from shop.models import *
from shop.views import list
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib import messages
import requests
import json


def order_create(request):
    [categories, suppliers, objectives, products_rec, offers] = list()
    cart = Cart(request)
    if not cart:
        messages.error(request, "Корзина пуста!")
        return redirect('cart:cart_detail')
    profile = Profile.published.get(user=request.user)
    data = {'first_name': profile.first_name,
            'last_name': profile.last_name,
            'email': profile.email,
            'address': profile.address,
            'city': profile.city,
            'postal_code': profile.postal_code,
            'phone': profile.phone}
    postal_code = ''
    if request.method == 'POST':
        if 'form' in request.POST:
            form = OrderCreateForm(request.POST, initial=data)
            order = form.save(commit=False)
        else:
            perm_form = PermOrderCreateForm(request.POST, initial=data)
            order = perm_form.save(commit=False)
        if cart.coupon:
            order.coupon = cart.coupon
            order.discount = cart.coupon.discount

        order.client = request.user
        order.status = 'Новый'
        order.save()
        # Высчитываем массу и создаём объекты заказа в функции calc_order_total_mass
        order.total_mass = calc_order_total_mass(cart, order)
        cart.clear()
        # Пробуем получить стоимость доставки по API почты России. 
        try:
            # если Пермь, то по дефолту будет стоить 200р. Если другой  населенный пункт,
            # то пробуем рассчитать через API почты
            if order.city != 'Пермь':
                order.deliver_cost = russian_post_calc(postal_code=order.postal_code, mass=order.total_mass)
        except:
            try:
                # если пользователь ввёл неверный индекс, то пробуем посчитать доставку до белгорода
                order.deliver_cost = russian_post_calc(postal_code='308000', mass=order.total_mass)
            except:
                # если пользователь ввёл неверный индекс и API почты не работает, то ставим среднюю доставку 350 р
                order.deliver_cost = 350
        order.save()
        messages.success(request, 'Заказ успешно создан.')
        messages.success(request, 'Оплатить заказ можно по форме ниже.')

        # Отправка письма администрации
        subject = 'Новый заказ'
        sender = 'no-reply@mrpit.online'
        message = 'Новый заказ!<br> Номер заказа:{}<br> Город: {}<br>' \
                  'Перейти в <a href="https://mrpit.online/admin/orders/order">Админку</a> для просмотра заказа. ' \
            .format(order.id, order.city)
        mail_admin = EmailMessage(subject, message, sender, ['admin@mrpit.online', 'nukez@inbox.ru'])
        mail_admin.content_subtype = "html"
        mail_admin.send()
        # Отправка письма Клиенту
        client_subject = 'Заказ с сайта MrPit.Online'
        mail_from = 'no-reply@mrpit.online'
        mail_to = [order.email]
        сlient_message = 'Спасибо за Ваш заказ!<br>Номер заказа:{}<br>' \
                         'Стоимость заказа:{} р., Стоимость доставки:{} р.' \
                         'Масса посылки с учетом упаковки:{} гр.<br>' \
                         'Оплатить заказ Вы можете на сайте в ' \
                         '<a href="https://mrpit.online/account">Личном Кабинете</a><br>' \
                         'После оплаты заказа мы начнём сборку. ' \
                         'Статус заказа Вы можете отслеживать также в личном кабинете.<br><br>' \
                         'Наши соцсети ждут именно Вас:<br>' \
                         '<a href="https://vk.com/mrpit.online">Вконтакте</a><br>' \
                         '<a href="https://instagram.com/mrpit.online">Instagram</a>' \
            .format(order.id, order.get_total_cost(), order.deliver_cost, order.total_mass)
        mail = EmailMessage(client_subject, сlient_message, mail_from, mail_to)
        mail.content_subtype = "html"
        mail.send()
        username = request.user.username
        # перенаправляем пользователя в личный кабинет, где он сможет оплатить заказ
        return redirect('profile')
    else:
        form = OrderCreateForm(initial=data)
        perm_form = PermOrderCreateForm(initial=data)
    template = 'orders/order/create.html'
    context = locals()
    return render(request, template, context)


@staff_member_required
def admin_order_detail(request, order_id):
    order = Order.published.get(id=order_id)
    if request.method == 'POST':
        order_form = TrackForm(request.POST)
        if order_form.is_valid():
            order.track_number = order_form.cleaned_data['track_number']
            if order.track_number != '':
                subject = 'Отправка заказа'
                mail_from = 'admin@mrpit.online'
                mail_to = [order.email]
                message = 'Спасибо за Ваш заказ!<br>' \
                          'Посылка сформирована и отправлена по адресу: {}, {}<br>' \
                          'Номер отслеживания: {}<br>' \
                          'Отследить посылку Вы можете на сайте <a href="https://www.pochta.ru">Почты России</a><br>' \
                          'По всем вопросам можете обращаться через ' \
                          '<a href="https://mrpit.online/feedback">форму обратной связи</a>,' \
                          ' либо можете ответить на это письмо.<br><br>' \
                          'Наши соцсети ждут именно Вас:<br>' \
                          '<a href="https://vk.com/mrpit.online">Вконтакте</a><br>' \
                          '<a href="https://instagram.com/mrpit.online">Instagram</a>' \
                    .format(order.city, order.address, order.track_number)
                mail = EmailMessage(subject, message, mail_from, mail_to)
                mail.content_subtype = "html"
                mail.send()
                order.status = 'Отправлен'
                order.save()
                messages.success(request, 'Письмо отправлено')
                return redirect('orders:admin_order_detail', order.id)
            else:
                messages.error(request, 'Сначала заполните номер отслеживания')
    else:
        form = TrackForm()

    template = 'admin/orders/order/detail.html'
    context = locals()
    return render(request, template, context)


def order_list(request, pk):
    [categories, suppliers, objectives, products_rec, offers] = list()
    order = Order.published.get(id=pk)
    items = order.items.all()
    template = 'orders/order/list.html'
    context = locals()
    return render(request, template, context)


def deny(request, order_id):
    [categories, suppliers, objectives, products_rec, offers] = list()
    order = Order.published.get(id=order_id)
    username = request.user.username
    template = 'orders/order/deny.html'
    context = locals()
    return render(request, template, context)


def denied(request, order_id):
    [categories, suppliers, objectives, products_rec, offers] = list()
    order = Order.published.get(id=order_id)
    order.status = 'Отказ'
    order.save()
    subject = 'Отмена заказа'
    sender = 'no-reply@mrpit.online'
    message = 'Отмена заказа!\n\n Номер заказа:{}\n Перейти в админку для просмотра заказа: {}' \
        .format(order.id, 'https://mrpit.online/admin/orders/order')
    send_mail(subject, message, sender, ['admin@mrpit.online', 'nukez@inbox.ru'])
    template = 'orders/order/deny_submit.html'
    context = locals()
    return render(request, template, context)


def order(request):
    username = request.user.username
    template = 'orders/order.html'
    context = locals()
    return render(request, template, context)


def repeat(request, order_id):
    order = Order.published.get(id=order_id)
    order_new = Order.published.create(deliver_cost=order.deliver_cost,
                                       first_name=order.first_name,
                                       last_name=order.last_name,
                                       email=order.email,
                                       address=order.address,
                                       postal_code=order.postal_code,
                                       phone=order.phone,
                                       city=order.city,
                                       total_mass=order.total_mass,
                                       status='Новый',
                                       client=order.client,
                                       paid=False)
    for item in order.items.all():
        OrderItem.published.create(order=order_new,
                                   flavour=item.flavour,
                                   price=item.price,
                                   quantity=item.quantity)
    order_new.total_cost = order.get_total_cost()
    order_new.save()
    messages.success(request, 'Заказ успешно создан.')
    messages.success(request, 'Оплатить заказ можно по форме ниже.')
    # отправка письма администрации
    subject = 'Новый заказ(повторный)'
    sender = 'no-reply@mrpit.online'
    message = 'Новый заказ!(повторный)<br> Номер заказа:{}<br> Город: {}<br>' \
              'Перейти в <a href="https://mrpit.online/admin/orders/order">Админку</a> для просмотра заказа. ' \
        .format(order.id, order.city)
    mail_admin = EmailMessage(subject, message, sender, ['admin@mrpit.online', 'nukez@inbox.ru'])
    mail_admin.content_subtype = "html"
    mail_admin.send()
    # отправка письма Клиенту
    client_subject = 'Заказ с сайта MrPit.Online'
    mail_from = 'no-reply@mrpit.online'
    mail_to = [order.email]
    сlient_message = 'Спасибо за Ваш заказ!<br>Номер заказа:{}<br>' \
                     'Стоимость заказа:{} р., Стоимость доставки:{} р.' \
                     'Масса посылки с учетом упаковки:{} гр.<br>' \
                     'Оплатить заказ Вы можете на сайте в ' \
                     '<a href="https://mrpit.online/account">Личном Кабинете</a><br>' \
                     'После оплаты заказа мы начнём сборку. ' \
                     'Статус заказа Вы можете отслеживать также в личном кабинете.<br><br>' \
                     'Наши соцсети ждут именно Вас:<br>' \
                     '<a href="https://vk.com/mrpit.online">Вконтакте</a><br>' \
                     '<a href="https://instagram.com/mrpit.online">Instagram</a>' \
        .format(order.id, order.get_total_cost(), order.deliver_cost, order.total_mass)
    mail = EmailMessage(client_subject, сlient_message, mail_from, mail_to)
    mail.content_subtype = "html"
    mail.send()
    return redirect('profile')


def russian_post_calc(postal_code, mass):
    token = RUSSIAN_POST_TOKEN
    key = RUSSIAN_POST_KEY
    host = "https://otpravka-api.pochta.ru"
    request_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json;charset=UTF-8",
        "Authorization": "AccessToken " + token,
        "X-User-Authorization": "Basic " + key
    }

    path = "/1.0/tariff"

    url = host + path

    try:
        destination = {
            "index-from": "614961",
            "index-to": postal_code,
            "mail-category": "ORDINARY",
            "mail-type": "POSTAL_PARCEL",
            "mass": mass,
            "fragile": "false"
        }
        response = requests.post(url, headers=request_headers, data=json.dumps(destination))
        decoder_json = json.loads(response.text)
        value = str(decoder_json['total-rate'] + decoder_json['total-vat'])
        value = int(value[0:-2])
        return value
    except:
        messages.error(request, message='Неверный индекс')
        return redirect('orders:create')


def calc_order_total_mass(cart, order):
    mass = 0
    total_mass = 0
    for item in cart:
        new_order_item = OrderItem.published.create(order=order,
                                                    flavour=item['flavour'],
                                                    price=item['price'],
                                                    quantity=item['quantity'])
        size = str(new_order_item.flavour.product.size)
        # Начинаем считать вес посылки, высчитывая вес каждой номенклатуры. Складываем граммы и мл одинаково
        if size[-2:] == 'гр' or size[-2:] == 'мл':
            if len(size) == 5:
                mass = int(size[0:2])
            elif len(size) == 6:
                mass = int(size[0:3])
            elif len(size) == 7:
                mass = int(size[0:4])
        # Тут принимаем одну таблетку или капсулу за 1 гр
        elif size[-4:] == 'капс' or size[-4:] == 'табл':
            if len(size) == 7:
                mass = int(size[0:2])
            elif len(size) == 8:
                mass = int(size[0:3])
            elif len(size) == 9:
                mass = int(size[0:4])
            # для остальных упаковок и пачек просто прибавляем 500 гр (упаковки, шейкеры)
        else:
            mass = 500
        if new_order_item.quantity > 1:
            mass *= new_order_item.quantity
        # прибавляем вес номенклатуры к общему весу посылки
        total_mass += mass
    # Прибавляем вес упаковки (пакет или мешок)
    total_mass += 200
    # Если посылка весит больше 2 кг, то её нужно упаковать в коробку, значит еще +200 гр
    if total_mass > 2000:
        total_mass += 200
    return total_mass
