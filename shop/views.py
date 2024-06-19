import uuid

from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet

from core.http_utils import HttpUtil
from core.permissions import IsShopOwner, IsShopManager, IsShopEmployee
from shop.models import Shop, Category, Inventory
from shop.serializers import ShopSerializer, CategorySerializer, InventorySerializer


class ShopApi(ViewSet):
    serializer_class = ShopSerializer
    permission_classes = [IsShopOwner]
    lookup_field = "guid"

    def list(self, request):
        shops = Shop.objects.filter(
            owner=request.user,
            status=True
        )
        shop_serializer = self.serializer_class(
            shops, many=True
        )
        return HttpUtil.success_response(
            data=shop_serializer.data,
            message="success"
        )

    def create(self, request):
        shop_serializer = self.serializer_class(
            data=request.data,
            context={"user": request.user}
        )
        if not shop_serializer.is_valid():
            return HttpUtil.error_response(
                shop_serializer.errors
            )
        shop_serializer.save(
            owner=request.user
        )
        return HttpUtil.success_response(
            data=shop_serializer.data,
            message="created",
            code=status.HTTP_201_CREATED
        )

    def retrieve(self, request, guid):
        try:
            shop = Shop.objects.get(
                guid=guid,
                owner=request.user,
                status=True
            )
            if shop:
                return HttpUtil.error_response(
                    message="shop not found!"
                )

            shop_serializer = ShopSerializer(shop)
            return HttpUtil.success_response(
                data=shop_serializer.data
            )
        except Shop.DoesNotExist:
            return HttpUtil.error_response(
                message="shop not found."
            )

    def update(self, request, guid):
        try:
            shop = Shop.objects.get(
                guid=guid,
                owner=request.user,
                status=True
            )
            shop_serializer = ShopSerializer(
                shop, data=request.data,
                context={"user": request.user}
            )
            if not shop_serializer.is_valid():
                return HttpUtil.error_response(
                    shop_serializer.errors
                )
            shop_serializer.save()

            return HttpUtil.success_response(
                data=shop_serializer.data
            )
        except Shop.DoesNotExist:
            return HttpUtil.error_response(
                message="shop not found."
            )

    def delete(self, request, guid):
        try:
            shop = Shop.objects.get(
                guid=guid,
                owner=request.user,
                status=True
            )
            shop.delete()
            return HttpUtil.success_response(
                message="deleted"
            )
        except Shop.DoesNotExist:
            return HttpUtil.error_response(
                message="shop not found."
            )


class CategoryApi(ViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsShopOwner]
    lookup_field = "guid"

    def list(self, request):
        categories = Category.objects.filter(
            created_by=request.user,
            status=True
        )
        category_serializer = self.serializer_class(
            categories, many=True
        )
        return HttpUtil.success_response(
            data=category_serializer.data,
            message="success"
        )

    def create(self, request):
        # if this category name exists
        if Category.objects.filter(
            created_by=request.user,
            name=request.data["name"]
        ).exists():
            return HttpUtil.error_response(
                message="name with this category already exists!"
            )

        category_serializer = self.serializer_class(
            data=request.data
        )
        if not category_serializer.is_valid():
            return HttpUtil.error_response(
                category_serializer.errors
            )

        category_serializer.save(
            created_by=request.user,
            status=True
        )
        return HttpUtil.success_response(
            data=category_serializer.data,
            message="created",
            code=status.HTTP_201_CREATED
        )

    def retrieve(self, request, guid):
        try:
            category = Category.objects.get(
                guid=guid,
                created_by=request.user,
                status=True
            )
            category_serializer = CategorySerializer(category)
            return HttpUtil.success_response(
                data=category_serializer.data
            )
        except Category.DoesNotExist:
            return HttpUtil.error_response(
                message="category not found."
            )

    def update(self, request, guid):
        try:
            category = Category.objects.get(
                guid=guid,
                created_by=request.user,
                status=True
            )
            category_serializer = CategorySerializer(
                category, data=request.data
            )
            if not category_serializer.is_valid():
                return HttpUtil.error_response(
                    category_serializer.errors
                )
            category_serializer.save()

            return HttpUtil.success_response(
                data=category_serializer.data
            )
        except Category.DoesNotExist:
            return HttpUtil.error_response(
                message="category not found."
            )

    def delete(self, request, guid):
        try:
            category = Category.objects.get(
                guid=guid,
                created_by=request.user,
                status=True
            )
            category.delete()
            return HttpUtil.success_response(
                message="deleted"
            )
        except Category.DoesNotExist:
            return HttpUtil.error_response(
                message="category not found."
            )


class InventoryApi(ViewSet):
    serializer_class = InventorySerializer
    permission_classes = [IsShopOwner | IsShopManager | IsShopEmployee]
    lookup_field = "guid"

    def list(self, request):
        shop_guid = request.query_params.get("shop_guid")
        inventories = Inventory.objects.filter(
            shop__guid=shop_guid,
            status=True
        )
        shop_serializer = self.serializer_class(
            inventories,
            many=True
        )
        return HttpUtil.success_response(
            data=shop_serializer.data
        )

    def create(self, request):
        shop = None

        if "created_by" not in request.data:
            request.data["created_by"] = request.user.pk

        if "status" not in request.data:
            request.data["status"] = True

        if "shop" in request.data:
            shop = Shop.objects.get(guid=request.data["shop"])
            if shop:
                request.data["shop"] = shop.pk

        inventory_serializer = self.serializer_class(
            data=request.data
        )
        if not inventory_serializer.is_valid():
            return HttpUtil.error_response(
                message=inventory_serializer.errors
            )

        inventory_serializer.save()
        return HttpUtil.success_response(
            message="success",
            code=status.HTTP_201_CREATED
        )