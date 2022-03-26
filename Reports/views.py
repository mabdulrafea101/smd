from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.db.models import Avg, Max, Min, Sum
from pytz import timezone
from Expenses.models import Expense
from Sales.models import Order
# Create your views here.

def date_filters(context):

    total_expense = Expense.objects.all().aggregate(Sum('expense_amount'))
    total_expense_paid = Expense.objects.exclude(is_paid=False).all().aggregate(Sum('expense_amount'))
    total_expense_unpaid = Expense.objects.filter(is_paid=False).all().aggregate(Sum('expense_amount'))
    context['order_count'] = Order.objects.all().count()
    order_paid = Order.objects.exclude(paid_amount=0).all().aggregate(Sum('paid_amount'))
    total_order_amount = Order.objects.all().aggregate(Sum('total_bill'))
    total_order_cost = Order.objects.all().aggregate(Sum('order_cost'))
    
    if total_order_cost['order_cost__sum']:
        context['orders_total_cost'] = total_order_cost['order_cost__sum']
    else:
        context['orders_total_cost'] = 0
    if total_expense['expense_amount__sum']:
        context['total_expense'] = total_expense['expense_amount__sum']
    else:
        context['total_expense'] = 0

    if total_expense_paid['expense_amount__sum']:
        context['total_expense_paid'] = total_expense_paid['expense_amount__sum']
    else:
        context['total_expense_paid'] = 0
    if total_expense_unpaid['expense_amount__sum']:
        context['total_expense_unpaid'] = total_expense_unpaid['expense_amount__sum']
    else:
        context['total_expense_unpaid'] = 0
    if order_paid['paid_amount__sum']:
        context['order_paid'] = order_paid['paid_amount__sum']
    else:
        context['order_paid'] = 0
    if total_order_amount['total_bill__sum']:
        context['total_order_amount'] = total_order_amount['total_bill__sum']
    else:
        context['total_order_amount'] = 0
    context['est_profit'] = context['total_order_amount'] - context['orders_total_cost'] - context['total_expense']
    context['pending_payment'] = context['total_order_amount'] -  context['order_paid']
    context['actual_profit'] = context['order_paid'] -  context['orders_total_cost'] - context['total_expense_paid']


class ReportsPage(LoginRequiredMixin, TemplateView):
    template_name = "Reports/reports_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_open'] = True
        date_filters(context)
        return context

    def post(self, request, *args, **kwargs):
        context = {}
        filter_date_start = request.POST.get("filter-start")
        filter_date_end = request.POST.get("filter-end")
        
        if filter_date_end == filter_date_start:
            today = datetime.date(datetime.now())
            yesterday = datetime.date(datetime.now()) - timedelta(days = 1)
            yesterday_24hr = str(yesterday) + " 23:59:59.000000"
            if filter_date_end == str(today):
                search_filter = [today, datetime.now()]
                print("today = ", search_filter)
            else:
                search_filter = [yesterday, yesterday_24hr]
                print("yesterday = ", search_filter)
        else:
            search_filter = [filter_date_start, str(filter_date_end + " 23:59:59.000000")]
            print("else = ", search_filter)
        if filter_date_start and filter_date_end:
            order_paid = Order.objects.exclude(paid_amount=0).all().aggregate(Sum('paid_amount'))
            context['range_orders'] = Order.objects.filter(created_at__range=search_filter).count()
            total_expense = Expense.objects.filter(updated_at__range=search_filter
            ).all().aggregate(Sum('expense_amount'))
            total_expense_paid = Expense.objects.exclude(is_paid=False).filter(updated_at__range=search_filter
            ).all().aggregate(Sum('expense_amount'))
            total_expense_unpaid = Expense.objects.filter(is_paid=False).filter(
                updated_at__range=search_filter
            ).all().aggregate(Sum('expense_amount'))
            
            order_paid = Order.objects.exclude(paid_amount=0).filter(
                created_at__range=search_filter
            ).all().aggregate(Sum('paid_amount'))
            
            t_total_order_amount = Order.objects.all().filter(
                created_at__range=search_filter
            ).aggregate(Sum('total_bill'))
            t_total_order_cost = Order.objects.all().filter(
                created_at__range=search_filter
            ).aggregate(Sum('order_cost'))

            if order_paid['paid_amount__sum']:
                context['order_paid'] = order_paid['paid_amount__sum']
            else:
                context['order_paid'] = 0
            if total_expense['expense_amount__sum']:
                context['t_total_expense'] = total_expense['expense_amount__sum']
            else:
                context['t_total_expense'] = 0
            if total_expense_paid['expense_amount__sum']:
                context['t_total_expense_paid'] = total_expense_paid['expense_amount__sum']
            else:
                context['t_total_expense_paid'] = 0
            
            if total_expense_unpaid['expense_amount__sum']:
                context['t_total_expense_unpaid'] = total_expense_unpaid['expense_amount__sum']
            else:
                context['t_total_expense_unpaid'] = 0

            if t_total_order_cost['order_cost__sum']:
                context['t_total_order_cost'] = t_total_order_cost['order_cost__sum']
            else:
                context['t_total_order_cost'] = 0
            if t_total_order_amount['total_bill__sum']:
                context['t_total_bill'] = t_total_order_amount['total_bill__sum']
            else:
                context['t_total_bill'] = 0

            context['t_est_profit'] = t_total_order_amount['total_bill__sum'] - context['t_total_order_cost'] - context['t_total_expense']
            context['t_pending_payment'] = t_total_order_amount['total_bill__sum'] -  context['order_paid']
            context['t_actual_profit'] = context['order_paid'] - context['t_total_order_cost'] - context['t_total_expense_paid']

        else:
            print("Date not selected.")
        date_filters(context)
        print("context == ", context)
        return render(request,self.template_name, context)
