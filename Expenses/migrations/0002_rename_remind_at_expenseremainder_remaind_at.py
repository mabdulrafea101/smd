# Generated by Django 3.2.6 on 2021-09-18 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Expenses', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expenseremainder',
            old_name='remind_at',
            new_name='remaind_at',
        ),
    ]
