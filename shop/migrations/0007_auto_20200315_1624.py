# Generated by Django 3.0.3 on 2020-03-15 11:24

from django.db import migrations, models
import easy_thumbnails.fields
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20200311_1539'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='offer',
            options={'ordering': ('sorting',), 'verbose_name': 'Предложение', 'verbose_name_plural': 'Предложения'},
        ),
        migrations.AddField(
            model_name='offer',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, upload_to=shop.models.upload_path_purpose),
        ),
        migrations.AddField(
            model_name='offer',
            name='sorting',
            field=models.IntegerField(default='1', verbose_name='Позиция в списке цели'),
        ),
    ]