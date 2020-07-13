# Generated by Django 3.0.6 on 2020-05-27 13:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20200526_2102'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscribe',
            options={'ordering': ('email',), 'verbose_name': 'Подписка на товар', 'verbose_name_plural': 'Подписки на товар'},
        ),
        migrations.AddField(
            model_name='lead',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата создания'),
            preserve_default=False,
        ),
    ]