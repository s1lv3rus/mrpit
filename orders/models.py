from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from shop.models import Flavour, Product
from phonenumber_field.modelfields import PhoneNumberField
from coupons.models import Coupon
from decimal import Decimal

from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()


class Order(models.Model):
    STATUS_CHOISES = (
        ('Новый', 'Новый'),
        ('В работе', 'В работе'),
        ('Отправлен', 'Отправлен'),
        ('Выполнен', 'Выполнен'),
        ('Отказ', 'Отказ'),
    )

    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email')
    address = models.CharField(max_length=250, verbose_name='Адрес')
    postal_code = models.CharField(max_length=20, verbose_name='Почтовый индекс')
    phone = models.BigIntegerField(verbose_name='Номер телефона')
    city = models.CharField(max_length=100, verbose_name='Населенный пункт', default='Пермь')
    status = models.CharField(max_length=50, choices=STATUS_CHOISES, verbose_name='Статус', blank=True)
    deliver_cost = models.IntegerField(verbose_name='Стоимость доставки', default=200)
    track_number = models.CharField(max_length=50, verbose_name='Номер отслеживания', default=' ', blank=True)
    client = models.ForeignKey(User, related_name='orders',
                               on_delete=models.CASCADE, default=True, verbose_name='Клиент')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False, verbose_name='Оплачен')
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL, verbose_name='Купон')
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)], verbose_name='Скидка')
    comment = models.CharField(max_length=250, verbose_name='Комментарий к заказу', blank=True)
    total_mass = models.IntegerField(default=2000,verbose_name='Масса заказа')
    published = PublishedManager()

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def discount_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return int(total_cost * (self.discount / Decimal('100')))

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))
    get_total_cost.short_description = 'Стоимость заказа'

    def get_absolute_url(self):
        return reverse('orders:orders', args=[self.pk])

    def order_items(self):
        items = OrderItem.published.filter(order=self)
        return items


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE,
                              verbose_name="Заказ",)
    flavour = models.ForeignKey(Flavour,
                                related_name='order_items',
                                on_delete=models.CASCADE,
                                verbose_name="Вкус",
                                blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    published = PublishedManager()

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
