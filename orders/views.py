from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import render, redirect
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


def order_create(request):
    [categories, suppliers, objectives, products_rec, offers] = list()
    cart = Cart(request)
    if not cart:
        messages.error(request, "Корзина пуста!")
        return redirect('cart:cart_detail')
    try:
        user = request.user
        profile = Profile.published.get(user=user)
        data = {'first_name': profile.first_name,
                'last_name': profile.last_name,
                'email': profile.email,
                'address': profile.address,
                'city': profile.city,
                'postal_code': profile.postal_code}

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
            subject = 'Новый заказ'
            sender = 'no-repeat@mrpit.online'
            message = 'Новый заказ!\n\n Номер заказа:{}\n Город: {}\n Перейти в админку для просмотра заказа: {}' \
                .format(order.id, order.city, 'http://mrpit.online/admin/orders/order')
            send_mail(subject, message, sender, ['admin@mrpit.online'])
            for item in cart:
                OrderItem.published.create(order=order,
                                           flavour=item['flavour'],
                                           price=item['price'],
                                           quantity=item['quantity'])
            cart.clear()
            messages.success(request, 'Заказ успешно создан.')
            messages.success(request, 'Ожидайте звонка менеджера.')
            messages.success(request, 'Оплатить заказ можно ниже по форме')
            username = request.user.username
            # redirect to lk
            return redirect('profile', username)
        else:
            form = OrderCreateForm(initial=data)
            perm_form = PermOrderCreateForm(initial=data)
        template = 'orders/order/create.html'
        context = locals()
        return render(request, template, context)
    except:
        template = 'orders/order/create.html'
        context = locals()
        return render(request, template, context)


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})


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
    sender = 'no-repeat@mrpit.online'
    message = 'Отмена заказа!\n\n Номер заказа:{}\n Перейти в админку для просмотра заказа: {}' \
        .format(order.id, order.city, 'http://mrpit.online/admin/orders/order')
    send_mail(subject, message, sender, ['admin@mrpit.online'])
    template = 'orders/order/deny_submit.html'
    context = locals()
    return render(request, template, context)


def order(request):
    username = request.user.username
    template = 'orders/order.html'
    context = locals()
    return render(request, template, context)
