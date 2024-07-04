from django.db import models

from users.abstract_models import BikreeBaseModelWithUser
from users.models import User


class Shop(BikreeBaseModelWithUser):
    name = models.CharField(max_length=50)
    address = models.TextField(null=True, blank=True)
    licence_no = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="store_owner"
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"uid: {self.uid} , name: {self.name}"


class Category(BikreeBaseModelWithUser):
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f"{self.name}"


class Inventory(BikreeBaseModelWithUser):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    total_stock = models.DecimalField(max_digits=20, decimal_places=3, default=0.00)
    position = models.CharField(max_length=100, null=True, blank=True)
    floor = models.CharField(max_length=100, null=True, blank=True)
    rack = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return f"shop {self.shop.name}: name {self.name}"


class BusinessPartnerAbstractModel(BikreeBaseModelWithUser):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.shop.name} {self.name}"


class Customer(BusinessPartnerAbstractModel):
    pass


class Vendor(BusinessPartnerAbstractModel):
    pass


class Sale(BikreeBaseModelWithUser):
    no = models.TextField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    total = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    total_paid = models.IntegerField(default=0, null=True, blank=True)
    total_payable = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.no


class SaleDetail(BikreeBaseModelWithUser):
    sale = models.ForeignKey(Sale, related_name="details", on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    qty = models.DecimalField(max_digits=20, decimal_places=3, default=0.00)
    price = models.DecimalField(max_digits=20, decimal_places=3, default=0.00)

    def __str__(self):
        return f"{self.sale.no} {self.inventory.name}"
