from django.forms import models

from core.base_abstract_models import BikreeBaseModel
from .models import User


class BikreeBaseModelWithUser(BikreeBaseModel):
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True