from django.db import models

from core.base_abstract_models import BikreeBaseModel
from .models import User


class BikreeBaseModelWithUser(BikreeBaseModel):
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_by"
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="updated_by"
    )

    class Meta:
        abstract = True