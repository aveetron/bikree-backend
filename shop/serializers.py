from typing import Dict, Any

from rest_framework import serializers

from users.abstract_serializers import BikreeBaseWithUserSerializer
from users.serializers import UserSerializer
from .models import Shop, Category, Inventory, Sale, SaleDetail, Customer


class SaleSerializerHelper:
    def __init__(self, obj: Any):
        self.obj = obj

    def get_shop(self) -> Dict[str, any]:
        return {
            "guid": self.obj.guid.hex if self.obj else None,
            "name": self.obj.name if self.obj else None
        }

    def get_created_by(self) -> Dict[str, any]:
        return {
            "guid": self.obj.guid.hex if self.obj else None,
            "name": f"{self.obj.first_name} {self.obj.last_name}" if self.obj else None,
            "role": self.obj.role.name if self.obj.role else None
        }


class ShopSerializer(BikreeBaseWithUserSerializer):
    name = serializers.CharField(required=False, allow_null=False)
    address = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    licence_no = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    owner = UserSerializer(read_only=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
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

    def create(self, validated_data: Dict[str, Any]) -> Shop:
        validated_data["owner"] = validated_data["owner"]
        validated_data["created_by"] = validated_data["owner"]
        validated_data["status"] = True
        return Shop.objects.create(**validated_data)

    def update(self, instance: Shop, validated_data: Dict[str, Any]) -> Shop:
        instance.name = validated_data.get("name", instance.name)
        instance.address = validated_data.get("address", instance.address)
        instance.licence_no = validated_data.get("licence_no", instance.licence_no)
        instance.save()
        return instance

    def to_representation(self, instance: Shop) -> Dict[str, Any]:
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


class InventorySerializer(serializers.ModelSerializer):
    guid = serializers.CharField(required=False,
                                 source="guid.hex",
                                 read_only=True)
    shop_guid = serializers.CharField(required=False,
                                      read_only=True,
                                      source="shop.guid.hex")
    shop_name = serializers.CharField(required=False,
                                      read_only=True,
                                      source="shop.name")

    class Meta:
        model = Inventory
        exclude = ["id"]

    def to_representation(self, instance: Inventory) -> Dict[str, Any]:
        representation = super().to_representation(instance)
        representation.pop('shop', None)  # Remove the 'shop' field from the representation
        return representation


class CustomerSerializer(serializers.ModelSerializer):
    guid = serializers.CharField(required=False,
                                 source="guid.hex",
                                 read_only=True)
    shop = serializers.SerializerMethodField(read_only=True)
    created_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Customer
        exclude = ["id"]

    def get_shop(self, obj: Customer) -> Dict[str, any]:
        helper = SaleSerializerHelper(obj.shop)
        return helper.get_shop()

    def get_created_by(self, obj: Sale) -> Dict[str, any]:
        helper = SaleSerializerHelper(obj.created_by)
        return helper.get_created_by()


class SaleDetailSerializer(serializers.ModelSerializer):
    guid = serializers.CharField(required=False, source="guid.hex")
    inventory = serializers.SerializerMethodField(
        read_only=True
    )

    class Meta:
        model = SaleDetail
        exclude = ["id", "sale", "created_at", "updated_at", "created_by", "updated_by"]

    def get_inventory(self, obj: SaleDetail) -> Dict[str, any]:
        return {
            "name": obj.inventory.name if obj.inventory else None,
            "description": obj.inventory.description if obj.inventory else None,
            "position": obj.inventory.position if obj.inventory else None,
            "floor": obj.inventory.floor if obj.inventory else None,
            "rack": obj.inventory.rack if obj.inventory else None
        }


class SaleSerializer(serializers.ModelSerializer):
    guid = serializers.CharField(required=False, source="guid.hex")
    shop = serializers.SerializerMethodField(read_only=True)
    details = SaleDetailSerializer(many=True, read_only=True)
    created_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Sale
        exclude = ["id"]

    def get_shop(self, obj: Sale) -> Dict[str, any]:
        helper = SaleSerializerHelper(obj.shop)
        return helper.get_shop()

    def get_created_by(self, obj: Sale) -> Dict[str, any]:
        helper = SaleSerializerHelper(obj.created_by)
        return helper.get_created_by()