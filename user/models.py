from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# from address.models import AddressField
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class ModelStateFieldsCacheDescriptor:
    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        res = instance.fields_cache = {}
        return res


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    username = models.CharField(_("user name"), unique=True, max_length=50)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_inventory_manager = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "email",
    ]

    objects = CustomUserManager()

    class Meta:
        app_label = "user"
        db_table = ""
        managed = True
        verbose_name = "system user"
        verbose_name_plural = "system users"
        order_with_respect_to = "is_staff"

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"


class Purchaser(models.Model):
    person_name = models.CharField(max_length=50, default=None, blank=True)
    email = models.EmailField(_("email address"), blank=True, unique=False)
    phone = PhoneNumberField(null=True, blank=True, unique=False)
    company_name = models.CharField(unique=True, blank=False, max_length=80)
    address = models.TextField(default=None, blank=True, max_length=255)

    class Meta:
        db_table = ""
        managed = True
        verbose_name = "Our Distributor"
        verbose_name_plural = "Our Distributors"

    def __str__(self):
        return str(self.company_name)


class Customer(models.Model):
    person_name = models.CharField(max_length=50, default=None, blank=True)
    email = models.EmailField(_("email address"), blank=True, unique=False)
    phone = PhoneNumberField(null=True, blank=True, unique=False)
    address = models.TextField(default=None, blank=True, max_length=255)

    class Meta:
        db_table = ""
        managed = True
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return str(self.person_name)
