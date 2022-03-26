# Generated by Django 3.2.6 on 2021-09-25 22:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_customer'),
        ('Sales', '0009_auto_20210925_2309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalorder',
            name='customer_phone_number',
        ),
        migrations.RemoveField(
            model_name='historicalorder',
            name='purchased_by',
        ),
        migrations.RemoveField(
            model_name='order',
            name='customer_phone_number',
        ),
        migrations.RemoveField(
            model_name='order',
            name='purchased_by',
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='customer',
            field=models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='user.customer'),
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='user.customer'),
        ),
    ]