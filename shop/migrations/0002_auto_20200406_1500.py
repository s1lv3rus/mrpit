# Generated by Django 3.0.3 on 2020-04-06 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flavour',
            options={'ordering': ('id',), 'verbose_name': 'Вкус', 'verbose_name_plural': 'Учет товаров'},
        ),
        migrations.RemoveField(
            model_name='flavour',
            name='supplier',
        ),
        migrations.AddField(
            model_name='product',
            name='purchase_price',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10, verbose_name='Закупочная цена'),
        ),
        migrations.AlterField(
            model_name='flavour',
            name='name',
            field=models.CharField(db_index=True, max_length=200, verbose_name='Вкус'),
        ),
    ]