from django import forms
from django.db import models
from django.forms import widgets
from django.forms.formsets import ORDERING_FIELD_NAME
from django.utils.translation import gettext_lazy as _

from .models import Product, ProductCategory


class ProductCategoryModelForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ["name", "description", "image"]
        labels = {
            "name": _("Category Name"),
            "description": _("Describe category purpose"),
            "image": _("Upload Image"),
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                }
            ),
        }


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "distributor",
            "product_code",
            "product_name",
            "product_category",
            "purchase_price",
            "sale_price",
            "description",
            "allow_pre_order",
            "image",
            "product_color",
        ]
        labels = {
            "product_code": _("Product Code"),
            "product_name": _("Product Name"),
            "product_category": _("Category"),
            "purchase_price": _("Purchase Price"),
            "sale_price": _("Sale Price"),
            "product_color": _("Product Color"),
            "description": _("Description"),
            "allow_pre_order": _("Allow Pre-order"),
            "image": _("Upload Image"),
        }
        error_messages = {
            "product_code": {
                "max_length": _("This Product's Code is too long."),
            },
            "product_name": {
                "max_length": _("This Product's name is too long."),
            },
            "description": {
                "max_length": _("This Product's name is too long."),
            },
        }
        widgets = {
            "product_code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Unique Code",
                }
            ),
            "product_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Product Name",
                }
            ),
            "product_category": forms.Select(
                attrs={
                    "class": "form-control",
                    }),
            "distributor": forms.Select(
                attrs={
                    "class": "form-control",
                    }),
            "purchase_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "name": "p_price",
                    "placeholder": "Rs.0000",
                }
            ),
            "sale_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "name": "s_price",
                    "placeholder": "Rs.0000",
                }
            ),
            
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write your Product Details...",
                }
            ),
            "product_color": forms.TextInput(
                attrs={
                    "class": "form-control",
                    
                }
            ),
            "allow_pre_order": forms.CheckboxInput(
                attrs={
                    "class": "form-control",
                    "id": "checkboxPrimary1",
                    "type": "checkbox",
                }
            ),
        }
