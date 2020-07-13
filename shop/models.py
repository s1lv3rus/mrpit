from django.utils import timezone

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from easy_thumbnails.fields import ThumbnailerImageField
from django.db.models import Q

from account.models import Profile


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()


def upload_path_author(instance, filename):
    return 'images/products/{0}/{1}'.format(instance.category, filename)


def upload_path_supplier(instance, filename):
    return 'images/supplier/{}'.format(filename)


def upload_path_purpose(instance, filename):
    return 'images/purpose/{}'.format(filename)


class SubCategory(models.Model):
    """Подкатегория товара"""
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    published = PublishedManager()

    class Meta:
        ordering = ('-name',)
        verbose_name = 'ПодКатегория'
        verbose_name_plural = 'ПодКатегории'

    def __str__(self):
        return self.name

    def products_by_subcategory(self):
        products = Product.published.filter(subcategory=self).exclude(available=False)
        return products


class Category(models.Model):
    """Категория товара"""
    subcategories = models.ManyToManyField(SubCategory)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    position = models.IntegerField(default='1', verbose_name='Позиция в списке категорий')
    description = RichTextUploadingField(blank=True, verbose_name='Описание')
    published = PublishedManager()

    class Meta:
        ordering = ('position',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

    def products_by_category(self):
        products = Product.published.filter(category=self).exclude(available=False)
        return products


class Supplier(models.Model):
    """Поставщики"""
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = ThumbnailerImageField(upload_to=upload_path_supplier, blank=True)
    description = RichTextUploadingField(blank=True, verbose_name='Описание')
    published = PublishedManager()

    class Meta:
        ordering = ('name',)
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_supplier', args=[self.slug])


class Product(models.Model):
    """Продукт"""
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='Категория')
    subcategory = models.ForeignKey(SubCategory, related_name='sub', on_delete=models.CASCADE,
                                    verbose_name='ПодКатегория')
    supplier = models.ForeignKey(Supplier, related_name='products_s', on_delete=models.CASCADE,
                                 verbose_name='Производитель')
    name = models.CharField(max_length=200, db_index=True, verbose_name='Имя')
    slug = models.SlugField(max_length=200, db_index=True)
    size = models.CharField(max_length=20, blank=True, verbose_name='Размер')
    image = ThumbnailerImageField(upload_to=upload_path_author, blank=True, verbose_name='Изображение')
    description = RichTextUploadingField(blank=True, verbose_name='Описание')
    sostav = ThumbnailerImageField(upload_to=upload_path_author, blank=True, verbose_name='Состав')
    body = RichTextUploadingField(blank=True, verbose_name='Применение')
    available = models.BooleanField(default=True, verbose_name='Доступен')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    recommendation = models.BooleanField(default=False, verbose_name='Рекомендация')
    published = PublishedManager()

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])

    def flavours_by_product(self):
        flavours = Flavour.published.filter(product=self)
        return flavours

    def flavour_by_product(self):
        flavour = Flavour.published.filter(product=self, for_offer=True).first()
        return flavour.id

    def flavour_for_gift(self):
        flavour = Flavour.published.filter(product=self).first()
        return flavour

    def price(self):
        flavour = Flavour.published.filter(product=self).first()
        return flavour.price

    def price2(self):
        flavour = Flavour.published.filter(product=self).first()
        return flavour.price2

    def quantity(self):
        flavours = Flavour.published.filter(product=self)
        quantity = 0
        for flavour in flavours:
            quantity += flavour.quantity
        return quantity


class Subscribe(models.Model):
    """Подписка на закончившийся товар"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    published = PublishedManager()
    email = models.EmailField("Email")

    class Meta:
        ordering = ('email',)
        verbose_name = "Подписка на товар"
        verbose_name_plural = "Подписки на товар"

    def __str__(self):
        return self.email


class Offer(models.Model):
    """Предложения для покупателя"""
    name = models.CharField("Название предложения", max_length=100)
    slug = models.SlugField(max_length=100, db_index=True)
    products = models.ManyToManyField(Product)
    sorting = models.IntegerField(default='1', verbose_name='Позиция в списке цели')
    description = RichTextUploadingField()
    image = ThumbnailerImageField(upload_to=upload_path_purpose, blank=True)
    calc = models.CharField("Для калькулятора", max_length=100, default='', blank=True)
    date = models.DateTimeField("Дата создания", auto_now_add=True)
    published = PublishedManager()

    class Meta:
        ordering = ('sorting',)
        verbose_name = "Предложение"
        verbose_name_plural = "Предложения"

    def __str__(self):
        return self.name

    def products_by_offer(self):
        products = Product.published.filter(offer=self)
        return products

    def price(self):
        products = Product.published.filter(offer=self)
        price = 0
        for product in products:
            price += product.price()
        return price


class Objective(models.Model):
    """Цели покупателея"""
    categories = models.ManyToManyField(Category, blank=True)
    offers = models.ManyToManyField(Offer, blank=True, related_name='offers')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = ThumbnailerImageField(upload_to=upload_path_purpose, blank=True)
    description = RichTextUploadingField(blank=True, verbose_name='Описание')
    published = PublishedManager()

    class Meta:
        ordering = ('name',)
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:objective_list', args=[self.slug])


class Flavour(models.Model):
    """Вкус у товара"""
    product = models.ForeignKey(Product, related_name='flavours', on_delete=models.CASCADE, verbose_name='Товар')
    name = models.CharField(max_length=200, db_index=True, verbose_name='Вкус')
    quantity = models.IntegerField(verbose_name='Количество')
    for_offer = models.BooleanField(verbose_name='Для офера', default=False)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=0, default=100, verbose_name='Закупочная цена')
    price = models.DecimalField(max_digits=10, decimal_places=0, default=100, verbose_name='Цена')
    price2 = models.DecimalField(max_digits=10, decimal_places=0, blank=True,
                                 null=True, verbose_name='Цена ранее(должна быть больше!')
    published = PublishedManager()
    objects = models.Manager()

    class Meta:
        ordering = ('id',)
        verbose_name = "Товар"
        verbose_name_plural = "Учет товаров"

    def __str__(self):
        return self.name

    def supplier(self):
        supplier = Product.published.get(flavours=self).supplier
        return supplier

    supplier.short_description = 'Производитель'

    def size(self):
        size = Product.published.get(flavours=self).size
        return size

    size.short_description = 'Размер'

    def percent(self):
        purchase_price = self.purchase_price
        price = self.price
        try:
            percent = str(int((price / purchase_price) * 100 - 100)) + '%'
        except:
            percent = 'на 0 делить нельзя'
        return percent

    percent.short_description = 'Процент накрутки'


class Comment(models.Model):
    """Комментарий к товару"""
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='user', verbose_name="Пользователь",
                               on_delete=models.CASCADE)
    body = models.TextField("Сообщение", max_length=500)
    date = models.DateTimeField("Дата отправки", auto_now_add=True)
    published = PublishedManager()

    class Meta:
        ordering = ('date',)
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.body

    def get_author_name(self):
        profile = Profile.published.get(user=self.author)
        return profile.first_name + ' ' + profile.last_name


class Article(models.Model):
    """Статьи о товарах"""
    name = models.CharField("Название статьи", max_length=100)
    slug = models.CharField(max_length=100)
    body = RichTextUploadingField()
    published = PublishedManager()

    class Meta:
        ordering = ('name',)
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('shop:article', args=[self.slug])



class News(models.Model):
    """Новости магазина"""
    name = models.CharField("Название новости", max_length=100)
    body = RichTextUploadingField()
    date = models.DateTimeField("Дата написания")
    published = PublishedManager()

    class Meta:
        ordering = ('-date',)
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.name


class Lead(models.Model):
    """Лиды"""
    name = models.CharField("Имя", max_length=100, default='Лид')
    email = models.EmailField("Email", blank=True, null=True)
    phone = models.BigIntegerField(verbose_name='Номер телефона', blank=True, null=True)
    created = models.DateTimeField("Дата создания", auto_now_add=True)
    published = PublishedManager()

    class Meta:
        ordering = ('-created',)
        verbose_name = "Лид"
        verbose_name_plural = "Лиды"

    def __str__(self):
        return self.name
