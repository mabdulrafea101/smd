# Generated by Django 3.2.6 on 2021-09-18 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0008_auto_20210918_1752'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalproduct',
            old_name='unit',
            new_name='p_unit',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='unit',
            new_name='p_unit',
        ),
    ]
