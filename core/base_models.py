import uuid

from django.db import models

from users.models import User


class BikreeBaseModel(models.Model):
    guid = models.UUIDField(
        default=uuid.uuid4, editable=False
    )
    # auto_now_add -> sets the field value only when the instance is created
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    # auto_now -> updates the field value every time the instance is saved
    updated_at = models.DateTimeField(
        auto_now=True
    )
    status = models.BooleanField(
        default=False
    )

    class Meta:
        abstract = True


class BikreeBaseClassWithUser(BikreeBaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True