from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView

from user.models import CustomUser, Customer, Purchaser

from .decorators import (admin_required, inventory_manager_required,
                         manager_required, staff_required)
from .forms import (AdminSignupForm, CustomerAddForm, InventoryManagerSignupForm,
                    ManagerSignupForm, PurchaserAddForm, StaffSignupForm)

# Create your views here.


# ---------------------------------------------------
#
#                   USERs
#
# ---------------------------------------------------
@login_required
@admin_required
def signup_admin(request):
    if request.method == "POST":
        form = AdminSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user-list")

    else:
        form = AdminSignupForm()
    context = {
        "form": form,
        "user_open": True
    }
    return render(request, "user/admin_signup.html", context)


@login_required
@admin_required
def signup_manager(request):
    if request.method == "POST":
        form = ManagerSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user-list")

    else:
        form = ManagerSignupForm()
    context = {
        "form": form,
        "user_open": True
    }
    return render(request, "user/manager_signup.html", context)


@login_required
@admin_required
def signup_inventory_manager(request):
    
    if request.method == "POST":
        form = InventoryManagerSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user-list")

    else:
        form = InventoryManagerSignupForm()
    context = {
        "form": form,
        "user_open": True
    }
    return render(request, "user/inventory_manager_signup.html", context)


@login_required
@admin_required
def signup_staff(request):
    if request.method == "POST":
        form = StaffSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user-list")

    else:
        form = StaffSignupForm()
    context = {
        "form": form,
        "user_open": True
    }
    return render(request, "user/staff_signup.html", context)


@login_required
@admin_required
def get_user_list(request):
    u = get_user_model()
    users = u.objects.all()
    context = {
        "object_list": users,
        "user_open": True
    }
    return render(request, "user/users_list.html", context)


@login_required
@admin_required
def activate_user(request, pk):
    u = get_user_model()
    user = u.objects.filter(pk=pk).get()
    user.is_active = True
    user.save()
    return redirect("user-list")


@login_required
@admin_required
def deactivate_user(request, pk):
    u = get_user_model()
    user = u.objects.filter(pk=pk).get()
    user.is_active = False
    user.save()
    return redirect("user-list")


@login_required
@admin_required
def user_active_list(request):
    u = get_user_model()
    users = u.objects.filter(is_active=True)
    return render(request, "user/users_list.html", context={"object_list": users})


@login_required
@admin_required
def user_blocked_list(request):
    u = get_user_model()
    users = u.objects.filter(is_active=False)
    return render(request, "user/users_list.html", context={"object_list": users})


@method_decorator([login_required, admin_required], name="dispatch")
class PurchaserAddView(CreateView):

    model = Purchaser
    form_class = PurchaserAddForm
    success_url = reverse_lazy("purchaser-list")
    template_name = "user/medical_store_signup.html"

    def get_context_data(self, **kwargs):
        context = super(PurchaserAddView, self).get_context_data(**kwargs)
        context['distributor_open'] = True
        return context


@method_decorator([login_required, admin_required], name="dispatch")
class PurchaserList(ListView):
    model = Purchaser
    context_object_name = "purchaser"
    template_name = "user/medical_store_list.html"

    def get_context_data(self, **kwargs):
        context = super(PurchaserList, self).get_context_data(**kwargs)
        context['distributor_open'] = True
        return context


@method_decorator([login_required, admin_required], name="dispatch")
class PurchaserDelete(DeleteView):
    model = Purchaser
    template_name = "user/medical_store_delete.html"
    success_url = reverse_lazy("purchaser-list")

    def get_context_data(self, **kwargs):
        context = super(PurchaserDelete, self).get_context_data(**kwargs)
        context['distributor_open'] = True
        return context


@method_decorator([login_required, admin_required], name="dispatch")
class PurchaserUpdate(UpdateView):
    model = Purchaser
    form_class = PurchaserAddForm
    template_name = "user/medical_store_edit.html"
    success_url = reverse_lazy("purchaser-list")

    def get_context_data(self, **kwargs):
        context = super(PurchaserUpdate, self).get_context_data(**kwargs)
        context['distributor_open'] = True
        return context


@method_decorator([login_required, admin_required], name="dispatch")
class CustomerAddView(CreateView):

    model = Customer
    form_class = CustomerAddForm
    success_url = reverse_lazy("order_add")
    template_name = "user/customer_signup.html"

    def get_context_data(self, **kwargs):
        context = super(CustomerAddView, self).get_context_data(**kwargs)
        context['customer_open'] = True
        return context


@method_decorator([login_required, admin_required], name="dispatch")
class CustomerList(ListView):
    model = Customer
    context_object_name = "customer"
    template_name = "user/customer_list.html"

    def get_context_data(self, **kwargs):
        context = super(CustomerList, self).get_context_data(**kwargs)
        context['customer_open'] = True
        return context


@method_decorator([login_required, admin_required], name="dispatch")
class CustomerDelete(DeleteView):
    model = Customer
    template_name = "user/customer_delete.html"
    success_url = reverse_lazy("customer-list")

    def get_context_data(self, **kwargs):
        context = super(CustomerDelete, self).get_context_data(**kwargs)
        context['customer_open'] = True
        return context


@method_decorator([login_required, admin_required], name="dispatch")
class CustomerUpdate(UpdateView):
    model = Customer
    form_class = CustomerAddForm
    template_name = "user/customer_edit.html"
    success_url = reverse_lazy("customer-list")

    def get_context_data(self, **kwargs):
        context = super(CustomerUpdate, self).get_context_data(**kwargs)
        context['customer_open'] = True
        return context
