from Expenses.forms import ExpenseCategoryModelForm, ExpenseModelForm
from Expenses.models import Expense, ExpenseCategory
from django.shortcuts import redirect, render
from django.views.generic import DeleteView, DetailView, ListView, UpdateView, FormView, CreateView
from django.db.models import Avg, Max, Min, Sum
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from user.decorators import (admin_required, inventory_manager_required,
                             manager_required, staff_required)

# Create your views here.

@method_decorator([login_required, manager_required], name="dispatch")
class ExpenseCategoryList(ListView):
    model = ExpenseCategory
    context_object_name = 'expense_category'
    template_name='Expenses/expense_category_list.html'

    def get_context_data(self, **kwargs):
        context = super(ExpenseCategoryList, self).get_context_data(**kwargs)
        e_category = ExpenseCategory.objects.all()
        context["title"] = "Expense Category"
        context["e_category"] = e_category
        context["expense_open"] = True
        return context


@method_decorator([login_required, manager_required], name="dispatch")
class AddExpenseCategoryView(FormView):
    model = ExpenseCategory
    form_class = ExpenseCategoryModelForm
    template_name='Expenses/add_expense_category.html'
    success_url = reverse_lazy("expenses_category_list")

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):

        print("-----------Expense category form is valid--------")
        form.save(commit=True)
        return super().form_valid(form)


@method_decorator([login_required, manager_required], name="dispatch")
class ExpenseCategoryUpdateView(UpdateView):
    model = ExpenseCategory
    form_class = ExpenseCategoryModelForm
    template_name='Expenses/add_expense_category.html'
    success_url = reverse_lazy("expenses_category_list")

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):

        print("-----------Expense category update form is valid--------")
        form.save(commit=True)
        return super().form_valid(form)


@method_decorator([login_required, manager_required], name="dispatch")
class ExpenseCategoryDetailView(DetailView):
    model = ExpenseCategory
    context_object_name = "expense_category"
    template_name='Expenses/expense_category_detail.html'

    def get_context_data(self, **kwargs):
        print(kwargs['object'])
        context = super().get_context_data(**kwargs)
        context["e_category"] = kwargs['object']
        context["expense_open"] = True
        return context


@login_required
@manager_required
def expense_category_delete(request, **kwargs):
    if request.method=="POST":
        e_category_id = request.POST.get('e_category')
        ExpenseCategory.objects.filter(id=e_category_id).delete()
        print("deleteing category now")

    return redirect(reverse_lazy("expenses_category_list"))


@method_decorator([login_required, manager_required], name="dispatch")
class ExpenseList(ListView):
    model = Expense
    context_object_name = 'expense'
    template_name='Expenses/expense_list.html'

    def get_context_data(self, **kwargs):
        context = super(ExpenseList, self).get_context_data(**kwargs)
        expenses = Expense.objects.all()
        expenses_amount = expenses.aggregate(Sum('expense_amount'))
        total_expense_paid = Expense.objects.exclude(is_paid=False).all().aggregate(Sum('expense_amount'))
        total_expense_unpaid = Expense.objects.filter(is_paid=False).all().aggregate(Sum('expense_amount'))

        context['total_expense'] = expenses_amount['expense_amount__sum']
        if context['total_expense'] == None:
            context['total_expense'] = 0
        context['total_expense_paid'] = total_expense_paid['expense_amount__sum']
        if context['total_expense_paid'] == None:
            context['total_expense_paid'] = 0
        context['total_expense_unpaid'] = total_expense_unpaid['expense_amount__sum']
        if context['total_expense_unpaid'] == None:
            context['total_expense_unpaid'] = 0
        context["title"] = "Expense"
        context["expenses"] = expenses
        context["expense_open"] = True
        return context


@method_decorator([login_required, manager_required], name="dispatch")
class AddExpenseView(FormView):
    model = Expense
    form_class = ExpenseModelForm
    template_name='Expenses/add_expense.html'
    success_url = reverse_lazy("expenses_list")

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):

        print("-----------Expense form is valid--------")
        form.save(commit=True)
        return super().form_valid(form)


@method_decorator([login_required, manager_required], name="dispatch")
class ExpenseUpdateView(UpdateView):
    model = Expense
    form_class = ExpenseModelForm
    template_name='Expenses/add_expense.html'
    success_url = reverse_lazy("expenses_list")

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):

        print("-----------Expense Update form is valid--------")
        form.save(commit=True)
        return super().form_valid(form)


@method_decorator([login_required, manager_required], name="dispatch")
class ExpenseDetailView(DetailView):
    model = Expense
    context_object_name = "expense"
    template_name='Expenses/expense_detail.html'

    def get_context_data(self, **kwargs):
        print(kwargs['object'])
        context = super().get_context_data(**kwargs)
        context["expense"] = kwargs['object']
        context["expense_open"] = True
        return context

@login_required
@manager_required
def expense_delete(request, **kwargs):
    if request.method=="POST":
        expense_id = request.POST.get('expense_id')
        Expense.objects.filter(id=expense_id).delete()
        print("deleteing expense now")

    return redirect(reverse_lazy("expenses_list"))
