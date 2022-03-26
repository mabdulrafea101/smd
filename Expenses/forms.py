from attr import attr
from django import forms
from django.db import models
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from .models import Expense, ExpenseCategory, ExpenseRemainder


class ExpenseCategoryModelForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ["name", "description"]
        labels = {
            "name": _("Category Name"),
            "description": _("Describe category purpose"),
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


class ExpenseModelForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            "expense_name",
            "expense_category",
            "expense_amount",
            "expense_description",
            "is_paid",
        ]

        widgets = {
            "expense_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g (July Rent)",
                }
            ),
            "expense_category": forms.Select(
                attrs={
                    "class": "form-control",
                    }),
            "expense_amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "name": "e_amount",
                    "placeholder": "Rs.0000",
                }
            ),
            "expense_description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write your Expense Details...",
                }
            ),
            "is_paid": forms.CheckboxInput(
                attrs={
                    
                }
            ),        
        }


# class ExpenseReminderModelForm(forms.ModelForm):
#     class Meta:
#         model = ExpenseRemainder
#         fields = [
#             "expense", 
#             "remaind_at",
#             ]
#         widgets = {
#             "expense": forms.Select(
#                 attrs={
#                     "class": "form-control",
#                 }
#             ),
#             "remaind_at": forms.DateTimeField(
#                 attrs={
#                     "class": "form-control",
#                 }
#             ),
#         }
