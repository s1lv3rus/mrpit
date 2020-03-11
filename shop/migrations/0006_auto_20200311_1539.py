# Generated by Django 3.0.3 on 2020-03-11 10:39

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20200311_1443'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='lead',
            managers=[
                ('published', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='lead',
            name='name',
            field=models.CharField(default='Лид', max_length=100, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Email'),
        ),
    ]
