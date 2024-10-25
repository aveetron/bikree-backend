from typing import Any, Dict

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework import serializers, status

from core.base_abstract_serializers import BikreeBaseSerializer

from .models import Role, User


class UserSerializer(BikreeBaseSerializer):
    uid = serializers.CharField(read_only=True, source="uid.hex")
    phone = serializers.CharField(allow_blank=False)
    first_name = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    last_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    date_joined = serializers.DateTimeField(required=False)
    confirm_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        phone = User.objects.filter(phone=attrs.get("phone")).exists()
        if phone:
            raise ValidationError(
                "User with phone exists", code=status.HTTP_403_FORBIDDEN
            )

        if attrs.get("password") != attrs.get("confirm_password"):
            raise ValidationError(
                "Password doesn't match!", code=status.HTTP_400_BAD_REQUEST
            )

        return super().validate(attrs)

    def create(self, validated_data: Dict[str, Any]) -> User:
        if validated_data.get("password") != validated_data.pop("confirm_password"):
            raise ValidationError(
                "Confirm password doesn't match", code=status.HTTP_403_FORBIDDEN
            )

        else:
            new_user = User(**validated_data)
            new_user.password = make_password(validated_data.get("password"))
            new_user.is_active = True
            new_user.status = True
            """
                by default the role of the user will be shop owner
            """
            try:
                new_user.role = Role.objects.get(name=Role.SHOP_OWNER)
            except Role.DoesNotExist:
                new_user.role = None

            new_user.save()
            return new_user

    def update(self, instance: User, validated_data: Dict[str, Any]) -> User:
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)

        instance.save()
        return instance
