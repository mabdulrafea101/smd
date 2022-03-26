from django.contrib import admin

from .models import Inventory, InventoryIn, InventoryOut, InventoryReturn, Product, ProductCategory

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductCategory)

admin.site.register(Inventory)
admin.site.register(InventoryIn)
admin.site.register(InventoryOut)
admin.site.register(InventoryReturn)
