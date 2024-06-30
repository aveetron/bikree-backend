import uuid

from django.db import models


class BikreeBaseModel(models.Model):
    uid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True
    )
    # auto_now_add -> sets the field value only when the instance is created
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    # auto_now -> updates the field value every time the instance is saved
    updated_at = models.DateTimeField(
        auto_now=True
    )
    deleted_at = models.DateTimeField(
        null=True, blank=True
    )

    class Meta:
        abstract = True
