# Generated by Django 3.2 on 2022-03-26 21:41

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaser',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None),
        ),
    ]