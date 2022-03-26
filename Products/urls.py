from django.urls import path

from . import views as v

urlpatterns = [
    path("", v.ProductList.as_view(), name="products_list"),
    path("<int:pk>/", v.ProductDetailView.as_view(), name="product_detail"),
    path("add/", v.AddProductView.as_view(), name="products_add"),
    path("edit/<int:pk>", v.ProductUpdateView.as_view(), name="product_edit"),
    path("delete/<int:pk>", v.inactive_product, name="inactive-product"),
    path("c/", v.ProductCategoryList.as_view(), name="products_category_list"),
    path(
        "c/<int:pk>/",
        v.ProductCategoryDetailView.as_view(),
        name="product_category_detail",
    ),
    path("c/add/", v.AddProductCategoryView.as_view(), name="products_category_add"),
    path("c/delete/<int:pk>", v.ProductCategoryDeleteView.as_view(), name="products_category_delete"),
    path("c/edit/<int:pk>", v.ProductCategoryUpdateView.as_view(), name="products_category_edit"),

    path("inventory/", v.InventoryList.as_view(), name="inventory_list"),
    path("inventory/add/<int:pk>/", v.add_inventory_qty, name="add-inventory"),
    path("inventory/sub/<int:pk>/", v.sub_inventory_qty, name="subtract-inventory"),
]
