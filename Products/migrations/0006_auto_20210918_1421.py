# Generated by Django 3.2.6 on 2021-09-18 09:21

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0005_auto_20210918_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalproduct',
            name='product_color',
            field=colorfield.fields.ColorField(default='#000000CC', max_length=18),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_color',
            field=colorfield.fields.ColorField(default='#000000CC', max_length=18),
        ),
    ]