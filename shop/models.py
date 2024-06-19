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
