from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Avg, Max, Min, Sum
from Expenses.models import Expense
from Products.models import Inventory, Product
from Sales.models import Order
from user.decorators import (admin_required, inventory_manager_required,
                             manager_required, staff_required)

# Create your views here.

#@method_decorator([login_required, admin_required], name="dispatch")
@login_required
@staff_required
def home(request):
    inventory_worth = 0
    today = [str(datetime.date(datetime.now())) + " 00:00:00.000000", str(datetime.now())]
    template_name = "Dashboard/index.html"
    inventory = Inventory.objects.exclude(product_quantity__lte=0).all()
    for inv in inventory.values('product_quantity','product'):
        product = Product.objects.filter(id=inv['product']).get()
        inventory_worth += (product.purchase_price *inv['product_quantity'])
        print("product = ", product.purchase_price)
        print("Inventory = ", inv['product_quantity'])
        print("Inventory Worth = ", inventory_worth)
    
    expense = Expense.objects.filter(updated_at__range=today
            ).all().aggregate(Sum('expense_amount'))
    orders = Order.objects.filter(created_at__range=today).all()
    order_count = orders.count()
    order_amount = orders.aggregate(Sum('total_bill'))
    context = {
        "dashboard_open": True,
        "orders": orders,
        "order_count": order_count,
        "expense": expense['expense_amount__sum'],
        "order_amount": order_amount['total_bill__sum'],
        "inventory_worth": inventory_worth,
    }
    print(today)
    return render(request, template_name, context)