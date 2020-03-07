from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from easy_thumbnails.fields import ThumbnailerImageField


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()


def upload_path_author(instance, filename):
    return 'images/products/{0}/{1}'.format(instance.category, filename)


def upload_path_supplier(instance, filename):
    return 'images/supplier/{}'.format(filename)


def upload_path_purpose(instance, filename):
    return 'images/purpose/{}'.format(filename)


# Подкатегория товара
class SubCategory(models.Model):
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
        products = Product.published.filter(subcategory=self)
        return products


# Категория товара
class Category(models.Model):
    subcategories = models.ManyToManyField(SubCategory)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = RichTextUploadingField(blank=True, verbose_name='Описание')
    published = PublishedManager()

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

    def products_by_category(self):
        products = Product.published.filter(category=self)
        return products


# Поставщики
class Supplier(models.Model):
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


# Товар
class Product(models.Model):
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
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='Цена')
    price2 = models.DecimalField(max_digits=10, decimal_places=0, default=None, blank=True,
                                 null=True, verbose_name='Цена ранее(должна быть больше!')
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

    def flavour_by_product(self):
        flavour = Flavour.published.filter(product=self, for_offer=True).first()
        return flavour.id


# Пакеты предложений
class Offer(models.Model):
    name = models.CharField("Название предложения", max_length=100)
    slug = models.SlugField(max_length=100, db_index=True)
    products = models.ManyToManyField(Product)
    description = RichTextUploadingField()
    date = models.DateTimeField("Дата создания", auto_now_add=True)
    published = PublishedManager()

    class Meta:
        ordering = ('name',)
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
            price += product.price
        return price


# Цели покупателя
class Objective(models.Model):
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


# Вкус у товара
class Flavour(models.Model):
    product = models.ForeignKey(Product, related_name='flavours', on_delete=models.CASCADE, verbose_name='Товар')
    supplier = models.ForeignKey(Supplier, related_name='supplier', on_delete=models.CASCADE,
                                 verbose_name='Производитель', blank=True, default=True)  # Для админки
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название вкуса')
    quantity = models.IntegerField(verbose_name='Количество')
    for_offer = models.BooleanField(verbose_name='Для офера', default=False)
    published = PublishedManager()

    class Meta:
        ordering = ('name',)
        verbose_name = "Вкус"
        verbose_name_plural = "Вкусы"

    def __str__(self):
        return self.name


# Коммент к товару
class Comment(models.Model):
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


# Статьи
class Article(models.Model):
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


# Новости
class News(models.Model):
    name = models.CharField("Название новости", max_length=100)
    body = RichTextUploadingField()
    date = models.DateTimeField("Дата написания", auto_now_add=True)
    published = PublishedManager()

    class Meta:
        ordering = ('name',)
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.name
