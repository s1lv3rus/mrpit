from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()


class Profile(models.Model):
    STATUS_CHOICES = (
        ('Новый покупатель', 'Новый покупатель'), ('Оптовый покупатель', 'Оптовый покупатель'),)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=20, verbose_name='Имя', blank=True)
    last_name = models.CharField(max_length=20, verbose_name='Фамилия', blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, blank=True)
    email = models.EmailField(blank=True)
    city = models.CharField(max_length=20, verbose_name='Населённый пункт', blank=True)
    address = models.CharField(max_length=100, verbose_name='Адрес', blank=True)
    postal_code = models.CharField(max_length=10, verbose_name='Почтовый индекс', blank=True)
    phone = models.BigIntegerField(verbose_name='Номер телефона', blank=True, null=True)
    published = PublishedManager()

    class Meta:
        ordering = ('user',)
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.first_name

    # из спеки по django добавил функцию автосоздания профиля после регистрации юзера
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.published.create(user=instance, status='Новый покупатель', email=instance.email)
    post_save.connect(create_user_profile, sender=User)
