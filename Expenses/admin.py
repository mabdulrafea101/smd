from django.contrib import admin
from .models import Expense, ExpenseCategory, ExpenseRemainder
# Register your models here.
admin.site.register(Expense)
admin.site.register(ExpenseCategory)
admin.site.register(ExpenseRemainder)
