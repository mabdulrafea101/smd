# Generated by Django 3.2.6 on 2021-09-21 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0014_auto_20210920_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inv_product', to='Products.product'),
        ),
        migrations.AlterField(
            model_name='inventoryin',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inv_in_product', to='Products.product'),
        ),
        migrations.AlterField(
            model_name='inventoryout',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inv_out_product', to='Products.product'),
        ),
        migrations.AlterField(
            model_name='inventoryreturn',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inv_return_product', to='Products.product'),
        ),
    ]
