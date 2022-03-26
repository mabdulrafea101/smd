#from typing import Any, Dict, List, Optional, Type

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, DetailView, ListView, UpdateView
from django.views.generic.edit import FormView, CreateView

#from Inventory.models import Inventory
from Products.forms import ProductCategoryModelForm, ProductModelForm
from user.decorators import (admin_required, inventory_manager_required,
                             manager_required, staff_required)

from .models import Inventory, Product, ProductCategory

# Create your views here.

@method_decorator([login_required, manager_required], name="dispatch")
class ProductList(ListView):
    model = Inventory
    context_object_name = "products"
    template_name = "Products/product_list.html"
    ordering = ['id']

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        inventory = Inventory.objects.all()
        context["inventory"] = inventory
        context["product_open"] = True
        context["items_open"] = True
        return context

@method_decorator([login_required, manager_required], name="dispatch")
class ProductDetailView(DetailView):

    model = Product
    context_object_name = "product"
    template_name = "Products/product_details.html"

    def get_context_data(self, **kwargs):
        print(kwargs['object'])
        context = super().get_context_data(**kwargs)
        context["product"] = kwargs['object']
        context["title"] = "Products"
        context["product_open"] = True
        context["items_open"] = True
        return context

@method_decorator([login_required, manager_required], name="dispatch")
class AddProductView(FormView):
    template_name = "Products/add_product.html"
    model = Product
    form_class = ProductModelForm
    success_url = reverse_lazy("products_list")

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):

        print("-----------form is valid--------")
        form.save(commit=False)
        form.instance.product_added_by = self.request.user
        s_price = form.cleaned_data.get("sale_price")
        p_price = form.cleaned_data.get("purchase_price")
        print("-----------FORM Sale Price--------")
        print(s_price)
        print("-----------FORM Purchase Price--------")
        print(p_price)

        if s_price > p_price:
            form.save(commit=True)
            Inventory.objects.get_or_create(
                pk=form.instance.id,
                product= form.instance,
                product_quantity=0,
                )
        else:
            context = {}
            context['message'] = "Sale price must be greater than Purchase price..."
            print(context)
            return super().form_invalid(form)

        return super().form_valid(form)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Product"
        context["items_open"] = True
        context["product_open"] = True
        return context

@method_decorator([login_required, manager_required], name="dispatch")
class ProductUpdateView(UpdateView):
    model = Product
    template_name = "Products/add_product.html"
    form_class = ProductModelForm
    success_url = reverse_lazy("products_list")

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):

        print("-----------Update product form is valid--------")
        form.save(commit=False)
        form.instance.product_added_by = self.request.user
        s_price = form.cleaned_data.get("sale_price")
        p_price = form.cleaned_data.get("purchase_price")
        print("-----------FORM Sale Price--------")
        print(s_price)
        print("-----------FORM Purchase Price--------")
        print(p_price)

        if s_price > p_price:
            form.save(commit=True)
        else:
            form.errors['message'] = "Sale price must be greater than Purchase price."
            error_msg = form.errors.get('message',)
            print(error_msg)
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Product"
        context["items_open"] = True
        context["product_open"] = True
        return context


@method_decorator([login_required, manager_required], name="dispatch")
class ProductDeleteView(DeleteView):

    model = Product
    template_name = "Products/product_delete.html"
    success_url = "/products/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Product"
        context["product_open"] = True
        context["items_open"] = True
        return context

@login_required
@manager_required
def inactive_product(request,*args, **kwargs):
    if request.method == 'POST':
        Inventory.objects.filter(product_id=kwargs["pk"]).update(is_active=False)
        Product.objects.filter(id=kwargs["pk"]).update(is_active=False)
        print(kwargs)

    return redirect(reverse_lazy("products_list"))


class ProductCategoryList(LoginRequiredMixin, ListView):
    model = ProductCategory
    context_object_name = "product_category"
    template_name = "Products/product_category_list.html"

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryList, self).get_context_data(**kwargs)
        context["categories"] = ProductCategory.objects.all()
        context["title"] = "Products Category"
        context["product_open"] = True
        context["categoires_open"] = True
        return context


@method_decorator([login_required, manager_required], name="dispatch")
class ProductCategoryDetailView(DetailView):

    model = ProductCategory
    context_object_name = "product_category_detail"
    template_name = "Products/product_category_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Products"
        context["product_open"] = True
        context["categoires_open"] = True
        return context


@method_decorator([login_required, manager_required], name="dispatch")
class AddProductCategoryView(FormView):
    model = ProductCategory
    template_name = "Products/add_product_category.html"
    form_class = ProductCategoryModelForm
    success_url = reverse_lazy("products_category_list")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Category"
        context["product_open"] = True
        context["categoires_open"] = True
        return context


@method_decorator([login_required, manager_required], name="dispatch")
class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = "Products/add_product_category.html"
    form_class = ProductCategoryModelForm
    success_url = reverse_lazy("products_category_list")


@method_decorator([login_required, manager_required], name="dispatch")
class ProductCategoryDeleteView(DeleteView):

    model = ProductCategory
    template_name = "Products/product_category_delete.html"
    success_url = "/products/c/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Product Category"
        context["product_open"] = True
        context["categoires_open"] = True
        return context


@method_decorator([login_required, manager_required], name="dispatch")
class InventoryList(ListView):

    model = Inventory
    context_object_name = "inventory"
    template_name = "Products/inventory_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Inventory"
        context["inventory_open"] = True
        return context

@login_required
def add_inventory_qty(request,*args, **kwargs):
    if request.method == 'POST':
        qty_to_add = request.POST.get("inv_quantity")
        inventory_qty = Inventory.objects.filter(id=kwargs['pk']).values_list("product_quantity")[0][0]
        updated_quantity = int(qty_to_add) + inventory_qty
        Inventory.objects.filter(id=kwargs["pk"]).update(product_quantity=updated_quantity)
        print("----------- INV QTY from DB----------")
        print(updated_quantity)

    return redirect(reverse_lazy("inventory_list"))

@login_required
def sub_inventory_qty(request,*args, **kwargs):
    if request.method == 'POST':
        qty_to_add = request.POST.get("inv_quantity")
        inventory_qty = Inventory.objects.filter(id=kwargs['pk']).values_list("product_quantity")[0][0]
        print("--------inv qty already--------")
        print(inventory_qty)
        updated_quantity = int(qty_to_add) - int(inventory_qty)
        Inventory.objects.filter(id=kwargs["pk"]).update(product_quantity=updated_quantity)
        print("----------- INV QTY from DB----------")
        print(updated_quantity)

    return redirect(reverse_lazy("inventory_list"))