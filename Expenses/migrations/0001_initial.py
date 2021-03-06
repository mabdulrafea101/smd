# Generated by Django 3.2.6 on 2021-09-18 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense_name', models.CharField(max_length=100)),
                ('expense_amount', models.PositiveIntegerField(default=0)),
                ('expense_description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Expense',
                'verbose_name_plural': 'Expenses',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ExpenseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Expense Category',
                'verbose_name_plural': 'Expense Categories',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ExpenseRemainder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remind_at', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('expese', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Expenses.expense')),
            ],
            options={
                'verbose_name': 'Expense Remainder',
                'verbose_name_plural': 'Expense Remainders',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='expense',
            name='expense_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Expenses.expensecategory'),
        ),
    ]
