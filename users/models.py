from django.contrib.auth.models import AbstractUser
from django.db import models

from core.base_abstract_models import BikreeBaseModel
from users.managers import CustomUserManager


class Role(BikreeBaseModel):
    ADMIN = "Admin"
    BUSINESS_ANALYST = "Business Analyst"
    SHOP_OWNER = "Shop Owner"
    SHOP_EMPLOYEE = "Shop Employee"
    SHOP_MANAGER = "Shop Manager"
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f"uid: {self.uid} name: {self.name}"


class User(AbstractUser, BikreeBaseModel):
    username = None
    phone = models.CharField(unique=True, max_length=30)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["-date_joined"]
        indexes = [
            models.Index(
                fields=[
                    "uid",
                ]
            ),
        ]

    objects = CustomUserManager()

    def __str__(self) -> str:
        return f"{self.phone} - {self.uid.hex}"
