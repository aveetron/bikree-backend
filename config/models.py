from django.db import models

from core.base_abstract_models import BikreeBaseModel


class Uom(BikreeBaseModel):
    name = models.CharField(
        max_length=30
    )

    def __str__(self) -> str:
        return self.name