from typing import Any, Dict

from rest_framework import serializers

from core.base_abstract_serializers import BikreeBaseModelSerializer
from core.serializer_helpers import (
    InventorySerializerHelper,
    ShopSerializerHelper,
    UserSerializerHelper,
)

from .models import Category, Customer, Inventory, Sale, SaleDetail, Shop


class ShopSerializer(BikreeBaseModelSerializer):
    owner = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Shop
        exclude = ["id", "created_by", "updated_by"]

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        name = attrs.get("name")
        owner = attrs.get("owner")
        address = attrs.get("address")
        licence_no = attrs.get("licence_no")
        attrs["name"] = name.lower()

        if not (name or address or licence_no):
            raise serializers.ValidationError("No data to change.")

        if not owner:
            # If owner is not passed in the data, use request.user
            owner = self.context["user"]
            attrs["owner"] = owner

        if name and owner:
            shop_exists = Shop.objects.filter(
                name__iexact=name, owner=owner, deleted_at__isnull=True
            ).exists()
            if shop_exists:
                raise serializers.ValidationError("Shop already exists")

        return attrs

    def create(self, validated_date):
        validated_date["created_by"] = self.context["user"]
        validated_date["owner"] = self.context["user"]
        return super().create(validated_date)

    def get_owner(self, obj):
        helper = UserSerializerHelper(obj.created_by)
        return helper.get_created_by()


class CategorySerializer(serializers.ModelSerializer):
    uid = serializers.CharField(required=False, source="uid.hex", read_only=True)

    def validate(self, attrs: Dict[str, Any]) -> dict[str, Any]:
        name = attrs.get("name").lower()
        user = self.context["user"]
        if Category.objects.filter(
            name=name, created_by=user, deleted_at__isnull=True
        ).exists():
            raise serializers.ValidationError("Name Already Exists!")

        attrs["name"] = name
        attrs["created_by"] = user
        return attrs

    class Meta:
        model = Category
        fields = ["uid", "name", "deleted_at"]


class InventorySerializer(serializers.ModelSerializer):
    uid = serializers.CharField(required=False, source="uid.hex", read_only=True)
    item = serializers.SerializerMethodField(required=False, read_only=True)
    store = serializers.SerializerMethodField(required=False, read_only=True)

    class Meta:
        model = Inventory
        exclude = ["id"]

    def validate(self, attrs):
        name = attrs.get("name", None)
        shop = attrs.get("shop", None)

        if name and shop:
            attrs["name"] = name.lower()
            if Inventory.objects.filter(
                    name=name, shop=shop).exists():
                raise serializers.ValidationError("Inventory Name Already Exists!")

        return attrs

    def to_representation(self, instance: Inventory) -> Dict[str, Any]:
        representation = super().to_representation(instance)
        representation.pop("updated_by", None)
        representation.pop("total_stock", None)
        representation.pop("position", None)
        representation.pop("rack", None)
        representation.pop("floor", None)
        representation.pop("created_by", None)
        representation.pop("deleted_at", None)
        representation.pop("name", None)
        representation.pop("description", None)
        representation.pop("shop", None)
        return representation

    def get_item(self, obj: Inventory) -> Dict:
        helper = InventorySerializerHelper(obj)
        return helper.get_inventory()

    def get_store(self, obj: Shop) -> Dict:
        helper = ShopSerializerHelper(obj.shop)
        return helper.get_shop()


class CustomerSerializer(serializers.ModelSerializer):
    uid = serializers.CharField(required=False, source="uid.hex", read_only=True)
    shop = serializers.SerializerMethodField(read_only=True)
    created_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Customer
        exclude = ["id"]

    def get_shop(self, obj: Customer) -> Dict[str, any]:
        helper = ShopSerializerHelper(obj.shop)
        return helper.get_shop()

    def get_created_by(self, obj: Sale) -> Dict[str, any]:
        helper = UserSerializerHelper(obj.created_by)
        return helper.get_created_by()


class SaleDetailSerializer(serializers.ModelSerializer):
    uid = serializers.CharField(required=False, source="uid.hex")
    inventory = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SaleDetail
        exclude = ["id", "sale", "created_at", "updated_at", "created_by", "updated_by"]

    def get_inventory(self, obj: SaleDetail) -> Dict[str, any]:
        helper = InventorySerializerHelper(obj.inventory)
        return helper.get_inventory()


class SaleSerializer(serializers.ModelSerializer):
    uid = serializers.CharField(required=False, source="uid.hex")
    shop = serializers.SerializerMethodField(read_only=True)
    details = SaleDetailSerializer(many=True, read_only=True)
    created_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Sale
        exclude = ["id"]

    def get_shop(self, obj: Sale) -> Dict[str, any]:
        helper = ShopSerializerHelper(obj.shop)
        return helper.get_shop()

    def get_created_by(self, obj: Sale) -> Dict[str, any]:
        helper = UserSerializerHelper(obj.created_by)
        return helper.get_created_by()
