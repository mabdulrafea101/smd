# Generated by Django 3.2.6 on 2021-09-18 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0010_auto_20210918_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalproduct',
            name='p_unit',
            field=models.CharField(choices=[('Quantity', 'Quantity'), ('Meters', 'Meters'), ('Yards', 'Yards')], max_length=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='p_unit',
            field=models.CharField(choices=[('Quantity', 'Quantity'), ('Meters', 'Meters'), ('Yards', 'Yards')], max_length=10),
        ),
    ]