from django.db import models
from django.db.models.base import Model

# Create your models here.

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=400, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Expense Category'
        verbose_name_plural = 'Expense Categories'


class Expense(models.Model):
    expense_category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    expense_name = models.CharField(max_length=100)
    expense_amount = models.PositiveIntegerField(default=0)
    expense_description = models.TextField(max_length=400, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.expense_name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'


class ExpenseRemainder(models.Model):
    expese = models.ForeignKey(Expense, on_delete=models.CASCADE)
    remaind_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Expense Remainder'
        verbose_name_plural = 'Expense Remainders'