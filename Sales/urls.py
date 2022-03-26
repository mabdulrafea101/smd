from django.urls import path

from . import views as v

urlpatterns = [
    path("", v.OrdersList.as_view(), name="orders_list"),
    path("add/", v.AddOrderView.as_view(), name="order_add"),
    path("detail/<int:pk>", v.OrderDetail.as_view(), name="order_detail"),
    # path("edit/<int:pk>", v.OrderUpdateView.as_view(), name="order_edit"),
    # path("delete/<int:pk>", v.OrderDeleteView.as_view(), name="order_delete"),
    path("add/customer", v.order_add_customer, name="order_add_customer"),
    path("print/<int:pk>", v.print_invoice, name="print-invoice"),
]
