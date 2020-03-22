# Generated by Django 3.0.3 on 2020-03-22 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20200307_0911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='deliver',
        ),
        migrations.AddField(
            model_name='order',
            name='deliver_cost',
            field=models.IntegerField(default=300, verbose_name='Стоимость доставки'),
        ),
    ]
