from typing import Dict, Any

from django.core.exceptions import ValidationError
from rest_framework import serializers, status

from config.models import Uom
from core.base_abstract_serializers import BikreeBaseSerializer


class UomSerializer(BikreeBaseSerializer):
    name = serializers.CharField(required=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        uom = Uom.objects.filter(
            name=attrs.get("name")
        ).exists()
        if uom:
            raise ValidationError(
                "Unit of measurement already exists", code=status.HTTP_403_FORBIDDEN
            )

        return super().validate(attrs)

    def create(self, validated_data: Dict[str, Any]) -> Uom:
        return Uom.objects.create(**validated_data)

    def update(self, instance, validated_data: Dict[str, Any]) -> Uom:
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance
