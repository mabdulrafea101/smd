from django.urls import path

from . import views as v

urlpatterns = [
    path("", v.ExpenseList.as_view(), name="expenses_list"),
    path("<int:pk>/", v.ExpenseDetailView.as_view(), name="expense_detail"),
    path("add/", v.AddExpenseView.as_view(), name="expense_add"),
    path("edit/<int:pk>", v.ExpenseUpdateView.as_view(), name="expense_edit"),
    path("delete/", v.expense_delete, name="expense_delete"),

    path("c/", v.ExpenseCategoryList.as_view(), name="expenses_category_list"),
    path(
        "c/<int:pk>/",
        v.ExpenseCategoryDetailView.as_view(),
        name="expense_category_detail",
    ),
    path("c/add/", v.AddExpenseCategoryView.as_view(), name="expense_category_add"),
    path("c/delete/", v.expense_category_delete, name="expenses_category_delete"),
    path("c/edit/<int:pk>", v.ExpenseCategoryUpdateView.as_view(), name="expense_category_edit"),

]