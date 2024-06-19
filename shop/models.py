from django.db import models

from users.abstract_models import BikreeBaseModelWithUser
from users.models import User


class Shop(BikreeBaseModelWithUser):
    name = models.CharField(max_length=50)
    address = models.TextField(null=True, blank=True)
    licence_no = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name="store_owner")

    def __str__(self):
        return f"guid: {self.guid} , name: {self.name}"


class Category(BikreeBaseModelWithUser):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name}"


class Inventory(BikreeBaseModelWithUser):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    total_stock = models.DecimalField(max_digits=20, decimal_places=3,
                                      default=0.00)
    position = models.CharField(max_length=100, null=True, blank=True)
    floor = models.CharField(max_length=100, null=True, blank=True)
    rack = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"shop {self.shop.name}: name {self.name}"




