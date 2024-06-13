from django.db.migrations import serializer

from core.base_abstract_serializers import BikreeBaseSerializer
from users.serializers import UserSerializer


class BikreeBaseWithUserSerializer(BikreeBaseSerializer):
    created_by = UserSerializer(required=False, read_only=True)
    updated_by = UserSerializer(required=False, read_only=True)

    class Meta:
        abstract = True