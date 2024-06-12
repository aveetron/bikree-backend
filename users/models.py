import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from core.base_models import BikreeBaseModel
from users.managers import CustomUserManager


class Role(BikreeBaseModel):
    ADMIN = "Admin"
    BUSINESS_ANALYST = "Business Analyst"
    SHOP_OWNER = "Shop Owner"
    SHOP_EMPLOYEE = "Shop Employee"
    SHOP_MANAGER = "Shop Manager"
    name = models.CharField(
        max_length=30
    )

    def __str__(self):
        return f"guid: {self.guid} name: {self.name}"


class User(AbstractUser):
    username = None
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    phone = models.CharField(unique=True, max_length=30)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE
    )

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["-date_joined"]
        indexes = [
            models.Index(
                fields=[
                    "guid",
                ]
            ),
        ]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} - {self.guid.hex}"
