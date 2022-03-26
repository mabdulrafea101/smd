from django.db import models
from simple_history.models import HistoricalRecords
from phonenumber_field.modelfields import PhoneNumberField
from sqlalchemy import null

from user.models import CustomUser, Customer
from Products.models import Inventory

# Create your models here.
PAYMENT_TYPE = (("Partially Paid", "installment"),("Full Payment", "full_payment"),("Unpaid", "unpaid"))
class Order(models.Model):
    invoice_num = models.CharField(max_length=50, default=0, unique=True)
    customer = models.ForeignKey(Customer, related_name='customer', on_delete=models.PROTECT, default=None)
    payment_type = models.CharField(max_length=14, choices=PAYMENT_TYPE)
    paid_amount = models.IntegerField(default=0)
    subtotal = models.IntegerField(default=0)
    total_bill = models.IntegerField(default=0)
    total_discount = models.IntegerField(default=0)
    gst_amount = models.PositiveIntegerField(default=0)
    order_cost = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.invoice_num) +str(" - ") + str(self.customer)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-updated_at']


class OrderProduct(models.Model):
    invoice_item = models.ForeignKey(Order, on_delete=models.PROTECT)
    purchased_product = models.ForeignKey(Inventory, on_delete=models.PROTECT)
    purchased_quantity = models.PositiveIntegerField()
    sold_at_price = models.PositiveIntegerField()
    product_discount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Single item in invoice'
        verbose_name_plural = 'Single item in invoices'

        ordering = ['-updated_at']


    def __str__(self):
        return (
            f"{self.invoice_item.invoice_num} - {self.purchased_product}"
        )