# Generated by Django 3.2.6 on 2021-09-25 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0016_auto_20210921_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalproduct',
            name='p_unit',
            field=models.CharField(choices=[('Quantity', 'Quantity'), ('Meters', 'Meters'), ('Yards', 'Yards'), ('Ft', 'ft')], max_length=8),
        ),
        migrations.AlterField(
            model_name='product',
            name='p_unit',
            field=models.CharField(choices=[('Quantity', 'Quantity'), ('Meters', 'Meters'), ('Yards', 'Yards'), ('Ft', 'ft')], max_length=8),
        ),
    ]
