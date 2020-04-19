from decimal import Decimal
from django.conf import settings
from shop.models import Product, Flavour
from coupons.models import Coupon


class Cart(object):

    def __init__(self, request):
        """Инициализация объекта корзины."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняем в сессии пустую корзину.
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # Сохраняем купон.
        self.coupon_id = self.session.get('coupon_id')

    def add(self, flavour, quantity=1, update_quantity=False):
        """Добавление товара в корзину или обновление его количества."""
        flavour_id = str(flavour.id)
        if flavour_id not in self.cart:
            self.cart[flavour_id] = {'quantity': 0, 'price': str(flavour.price)}
        if update_quantity:
            self.cart[flavour_id]['quantity'] = quantity
        else:
            self.cart[flavour_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Помечаем сессию как измененную
        self.session.modified = True

    def remove(self, flavour):
        """Удаление товара из корзины."""
        flavour_id = str(flavour.id)
        if flavour_id in self.cart:
            del self.cart[flavour_id]
            self.save()

    def __iter__(self):
        """Проходим по товарам корзины и получаем соответствующие объекты Product"""
        flavour_ids = self.cart.keys()
        # get the product objects and add them to the cart
        flavours = Flavour.published.filter(id__in=flavour_ids)
        cart = self.cart.copy()
        for flavour in flavours:
            cart[str(flavour.id)]['flavour'] = flavour

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Возвращает общее количество товаров в корзине."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def clear(self):
        # Очистка корзины.
        del self.session[settings.CART_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.published.get(id=self.coupon_id)
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
