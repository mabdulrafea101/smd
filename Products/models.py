from django.db import models
from colorfield.fields import ColorField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.urls import reverse
from simple_history.models import HistoricalRecords
from user.models import CustomUser, Purchaser

# Create your models here.

class ProductCategory(models.Model):

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('-created_at',)


    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300, null=True, blank=True)
    image = models.ImageField(upload_to="categories/products/", null=True, default="default_img.jpg")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

class AbstractProduct(models.Model):
    class Meta:
        abstract = True
        
    distributor = models.ForeignKey(Purchaser, blank=True, on_delete=models.SET_NULL, null=True)
    product_code = models.CharField(max_length=30, unique=True)
    product_name = models.CharField(max_length=50)
    product_added_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, blank=True)
    slug = models.SlugField(null=True)
    purchase_price = (
        models.PositiveIntegerField()
    )  # TODO: function to write in inventory model for updated purchase price as it can vary for new arrival of stock.
    sale_price = models.PositiveIntegerField()
    allow_pre_order = models.BooleanField(default=False)
    product_color = models.CharField(max_length=9, default="#000000CC")
    product_category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    description = models.TextField(max_length=300, null=True, blank=True)
    image = models.ImageField(upload_to="products/", null=True, blank=True) #FIXME: default="default_img.jpg"
    is_never_sold = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(inherit=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name

UNIT = (("Quantity", "Quantity"),("Meters", "Meters"), ("Yards", "Yards"), ("Ft", "ft"))
class Product(AbstractProduct):

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ('-created_at',)

    p_unit = models.CharField(max_length=8, default="Unit")



class AbstractInventory(models.Model):

    product_quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(inherit=True)

    class Meta:
        db_table = ""
        managed = True
        abstract = True
        verbose_name = "Inventory"
        verbose_name_plural = "Inventories"



    def get_purchase_price(self):
        return self.purchase_price * self.quantity

    def get_sale_price(self):
        return self.sale_price * self.quantity


class Inventory(AbstractInventory): # actually this is Inventory
    product = models.ForeignKey(Product, related_name="inv_prod", null=True, on_delete=models.CASCADE, blank=True)
    is_never_sold = models.BooleanField(default=True)

    class Meta:
        db_table = ""
        managed = True
        verbose_name = "Inventory"
        verbose_name_plural = "Inventories"

    def __str__(self):
        return f"{self.product.product_name} - {self.product.product_category}"


class InventoryIn(AbstractInventory): # actually this is InventoryIn
    is_never_sold = models.BooleanField(default=True)
    is_inventory_returned = models.BooleanField(default=False)
    added_by_user = models.ForeignKey(
        CustomUser, null=True, related_name="added_by_user", on_delete=models.CASCADE
    )

    class Meta:
        db_table = ""
        managed = True
        verbose_name = "Inventory In"
        verbose_name_plural = "Inventories In"

    def __str__(self):
        display_time = str(self.updated_at.time()).split(".")[0]
        return f"{self.product.product_name} - {display_time}"

class InventoryReturn(AbstractInventory): # actually this is InventoryIn

    is_inventory_returned = models.BooleanField(default=True)
    returned_by_user = models.ForeignKey(
        CustomUser, null=True, related_name="returned_by_user", on_delete=models.CASCADE
    )


    class Meta:
        db_table = ""
        managed = True
        verbose_name = "Inventory Return"
        verbose_name_plural = "Inventories Return"

    def __str__(self):
        display_time = str(self.updated_at.time()).split(".")[0]
        return f"{self.product.product_name} --> {self.returned_by_user} --> {display_time}"

class InventoryOut(AbstractInventory): # actually this is InventoryOut

    taken_by_user = models.ForeignKey(
        CustomUser, null=True, related_name="taken_by_user", on_delete=models.CASCADE
    )

    class Meta:
        db_table = ""
        managed = True
        verbose_name = "Inventory Out"
        verbose_name_plural = "Inventories Out"

    def __str__(self):
        display_time = str(self.updated_at.date()).split(".")[0] + "-->" + str(self.updated_at.time()).split(".")[0]
        return f"{self.taken_by_user} - {display_time}"


def save_inventory_from_product(sender, instance, created, **kwargs):

    Inventory.objects.get_or_create(
    pk=instance.id,
    product= instance,
    product_quantity=0,
    )
#post_save.connect(save_inventory_from_product, sender=Product)