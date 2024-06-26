import decimal

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from core.http_utils import HttpUtil
from core.permissions import IsShopOwner, IsShopManager, IsShopEmployee
from shop.models import Shop, Category, Inventory, Sale
from shop.serializers import ShopSerializer, CategorySerializer, InventorySerializer, SaleSerializer, \
    SaleDetailSerializer


class ShopApi(ViewSet):
    serializer_class = ShopSerializer
    permission_classes = [IsShopOwner]
    lookup_field = "guid"

    def list(self, request: Request) -> Response:
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

    def create(self, request: Request) -> Response:
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

    def retrieve(self, request: Request, guid: str = None) -> Response:
        try:
            shop = Shop.objects.get(
                guid=guid,
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

    def update(self, request: Request, guid: str = None) -> Response:
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

    def delete(self, request: Request, guid: str = None) -> Response:
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

    def list(self, request: Request) -> Response:
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

    def create(self, request: Request) -> Response:
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

    def retrieve(self, request: Request, guid: str = None) -> Response:
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

    def update(self, request: Request, guid: str = None) -> Response:
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

    def delete(self, request: Request, guid: str = None) -> Response:
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

    def list(self, request: Request) -> Response:
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

    def create(self, request: Request) -> Response:
        shop = None

        if "created_by" not in request.data:
            request.data["created_by"] = request.user.pk

        if "status" not in request.data:
            request.data["status"] = True

        if "shop_guid" in request.data:
            shop = Shop.objects.get(guid=request.data["shop_guid"],
                                    status=True)
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

    def retrieve(self, request: Request, guid: str = None) -> Response:
        try:
            inventory = Inventory.objects.get(
                guid=guid,
                status=True
            )
            inventory_serializer = self.serializer_class(
                inventory, many=False
            )
            return HttpUtil.success_response(
                data=inventory_serializer.data
            )

        except Inventory.DoesNotExist:
            return HttpUtil.error_response(
                "Inventory doesn't found!"
            )

    def update(self, request: Request, guid: str = None) -> Response:
        try:
            inventory = Inventory.objects.get(
                guid=guid,
                status=True
            )
            if 'name' not in request.data:
                request.data['name'] = inventory.name

            if 'created_by' not in request.data:
                request.data['created_by'] = inventory.created_by.id

            if 'shop' not in request.data:
                request.data['shop'] = inventory.shop.id

            inventory_serializer = self.serializer_class(
                inventory, data=request.data
            )
            if not inventory_serializer.is_valid():
                return HttpUtil.error_response(
                    message=inventory_serializer.errors
                )

            inventory_serializer.save(
                updated_by=request.user
            )
            return HttpUtil.success_response(
                data=inventory_serializer.data,
                message="updated"
            )

        except Inventory.DoesNotExist:
            return HttpUtil.error_response(
                "Inventory doesn't found!"
            )

    def delete(self, request: Request, guid: str = None) -> Response:
        try:
            inventory = Inventory.objects.get(
                guid=guid,
                status=True
            )
            inventory.delete()
            return HttpUtil.success_response(
                message="deleted"
            )

        except Inventory.DoesNotExist:
            return HttpUtil.error_response(
                "Inventory doesn't found!"
            )


class StockEntryApi(ViewSet):
    serializer_class = InventorySerializer
    permission_classes = [IsShopOwner | IsShopManager | IsShopEmployee]
    lookup_field = "guid"

    def update(self, request: Request, guid: str = None) -> Response:
        try:
            inventory = Inventory.objects.get(
                guid=guid,
                status=True,
                shop__guid=request.query_params.get("shop_guid")
            )

            if "total_stock" not in request.data:
                return HttpUtil.error_response(message="stock qty missing.")

            request.data["total_stock"] = decimal.Decimal(request.data["total_stock"]) + decimal.Decimal(
                inventory.total_stock)

            # Ensure required fields have default values
            data = request.data.copy()
            data.setdefault('name', inventory.name)
            data.setdefault('created_by', inventory.created_by.id if inventory.created_by else None)
            data.setdefault('shop', inventory.shop.id if inventory.shop else None)

            # Update the inventory item
            inventory_serializer = self.serializer_class(inventory, data=data)
            if not inventory_serializer.is_valid():
                return HttpUtil.error_response(message=inventory_serializer.errors)

            inventory_serializer.save()
            return HttpUtil.success_response(message="Inventory updated successfully.")

        except Inventory.DoesNotExist:
            return HttpUtil.error_response(
                message="inventory item not found!"
            )


class StockOutApi(ViewSet):
    serializer_class = InventorySerializer
    permission_classes = [IsShopOwner | IsShopManager | IsShopEmployee]
    lookup_field = "guid"

    def update(self, request: Request, guid: str = None) -> Response:
        try:
            inventory = Inventory.objects.get(
                guid=guid,
                status=True,
                shop__guid=request.query_params.get("shop_guid")
            )

            if "total_stock" not in request.data:
                return HttpUtil.error_response(message="stock qty missing.")

            if decimal.Decimal(request.data["total_stock"]) > decimal.Decimal(inventory.total_stock):
                return HttpUtil.error_response(
                    message="you don't have enough stock"
                )

            request.data["total_stock"] = decimal.Decimal(
                inventory.total_stock) - decimal.Decimal(request.data["total_stock"])

            # Ensure required fields have default values
            data = request.data.copy()
            data.setdefault('name', inventory.name)
            data.setdefault('created_by', inventory.created_by.id if inventory.created_by else None)
            data.setdefault('shop', inventory.shop.id if inventory.shop else None)

            # Update the inventory item
            inventory_serializer = self.serializer_class(inventory, data=data)
            if not inventory_serializer.is_valid():
                return HttpUtil.error_response(message=inventory_serializer.errors)

            inventory_serializer.save()
            return HttpUtil.success_response(message="Inventory updated successfully.")

        except Inventory.DoesNotExist:
            return HttpUtil.error_response(
                message="inventory item not found!"
            )


class SaleApi(ViewSet):
    permission_classes = [IsShopOwner | IsShopEmployee | IsShopManager]
    sale_serializer_class = SaleSerializer
    sale_detail_serializer = SaleDetailSerializer
    lookup_field = "guid"

    def list(self, request: Request) -> Response:
        shop_guid = request.query_params.get("shop_guid", None)
        if not shop_guid:
            return HttpUtil.error_response(
                message="shop missing"
            )

        sales = Sale.objects.filter(
            shop__guid=shop_guid,
            status=True
        )
        sale_serializer = self.sale_serializer_class(
            sales, many=True
        )
        return HttpUtil.success_response(
            data=sale_serializer.data
        )

    def create(self, request: Request) -> Response:
        payload = request.data
        sale_serializer = self.sale_serializer_class(
            data=payload
        )
        if not sale_serializer.is_valid():
            return HttpUtil.error_response(
                message=sale_serializer.errors
            )
        sale_serializer.save()
        return HttpUtil.success_response(
            message="sale created",
            code=status.HTTP_201_CREATED
        )

    def retrieve(self, request: Request, guid: str) -> Response:
        try:
            sale = Sale.objects.get(
                guid=guid,
                status=True
            )
        except Sale.DoesNotExist:
            return HttpUtil.error_response(
                message="sale doesn't exists!"
            )

        sale_serializer = self.sale_serializer_class(
            sale, many=False
        )
        return HttpUtil.success_response(
            data=sale_serializer.data
        )
