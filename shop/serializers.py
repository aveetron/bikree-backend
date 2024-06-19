from rest_framework import serializers

from users.abstract_serializers import BikreeBaseWithUserSerializer
from users.serializers import UserSerializer
from .models import Shop, Category


class ShopSerializer(BikreeBaseWithUserSerializer):
    name = serializers.CharField(required=False, allow_null=False)
    address = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    licence_no = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    owner = UserSerializer(read_only=True)

    def validate(self, attrs):
        name = attrs.get("name")
        owner = attrs.get("owner")
        address = attrs.get("address")
        licence_no = attrs.get("licence_no")

        if not (name or address or licence_no):
            raise serializers.ValidationError("No data to change.")

        if not owner:
            # If owner is not passed in the data, use request.user
            owner = self.context['user']

        if name and owner:
            shop_exists = Shop.objects.filter(name=name, owner=owner).exists()
            if shop_exists:
                raise serializers.ValidationError("Shop already exists")

        return attrs

    def create(self, validated_data):
        validated_data["owner"] = validated_data["owner"]
        validated_data["created_by"] = validated_data["owner"]
        validated_data["status"] = True
        return Shop.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.address = validated_data.get("address", instance.address)
        instance.licence_no = validated_data.get("licence_no", instance.licence_no)
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        exclude_fields = ['created_by', 'updated_by']  # Add any fields you want to exclude here
        for field in exclude_fields:
            data.pop(field, None)
        return data


class CategorySerializer(serializers.ModelSerializer):
    guid = serializers.CharField(required=False,
                                 source="guid.hex",
                                 read_only=True)

    class Meta:
        model = Category
        fields = [
            "guid", "name", "status"
        ]