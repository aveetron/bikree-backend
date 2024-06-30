from django.db import models

from core.base_abstract_models import BikreeBaseModel
from .models import User


class BikreeBaseModelWithUser(BikreeBaseModel):
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_created"
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
    )

    class Meta:
        abstract = True
