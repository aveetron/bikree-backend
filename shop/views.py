import decimal
from typing import Union

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from core.http_utils import HttpUtil
from core.permissions import IsShopEmployee, IsShopManager, IsShopOwner
from core.utils import soft_delete
from shop.models import Category, Customer, Inventory, Sale, SaleDetail, Shop
from shop.serializers import (
    CategorySerializer,
    CustomerSerializer,
    InventorySerializer,
    SaleDetailSerializer,
    SaleSerializer,
    ShopSerializer,
)


class ShopApi(ViewSet):
    serializer_class = ShopSerializer
    permission_classes = [IsShopOwner]
    lookup_field = "uid"

    def list(self, request: Request) -> Response:
        shops = Shop.objects.filter(owner=request.user, deleted_at__isnull=True)
        if request.query_params.get("shop_name", None):
            shops = shops.filter(name__icontains=request.query_params.get("shop_name"))

        shop_serializer = self.serializer_class(shops, many=True)
        return HttpUtil.success_response(data=shop_serializer.data, message="success")

    def create(self, request: Request) -> Response:
        shop_serializer = self.serializer_class(
            data=request.data, context={"user": request.user}
        )
        if not shop_serializer.is_valid():
            return HttpUtil.error_response(shop_serializer.errors)
        shop_serializer.save()
        return HttpUtil.success_response(
            data=shop_serializer.data, message="created", code=status.HTTP_201_CREATED
        )

    def retrieve(self, request: Request, uid: str = None) -> Response:
        try:
            shop = Shop.objects.get(uid=uid, deleted_at__isnull=True)
            if not shop:
                return HttpUtil.error_response(message="shop not found!")

            shop_serializer = ShopSerializer(shop)
            return HttpUtil.success_response(data=shop_serializer.data)
        except Shop.DoesNotExist:
            return HttpUtil.error_response(message="shop not found.")

    def update(self, request: Request, uid: str = None) -> Response:
        try:
            shop = Shop.objects.get(
                uid=uid, owner=request.user, deleted_at__isnull=True
            )
            shop_serializer = ShopSerializer(
                shop, data=request.data, context={"user": request.user}, partial=True
            )
            if not shop_serializer.is_valid():
                return HttpUtil.error_response(shop_serializer.errors)
            shop_serializer.save()
            return HttpUtil.success_response(data=shop_serializer.data)
        except Shop.DoesNotExist:
            return HttpUtil.error_response(message="shop not found.")

    def delete(self, request: Request, uid: str = None) -> Response:
        try:
            shop = Shop.objects.get(
                uid=uid, owner=request.user, deleted_at__isnull=True
            )
            soft_delete(shop)
            return HttpUtil.success_response(message="deleted")
        except Shop.DoesNotExist:
            return HttpUtil.error_response(message="shop not found.")


class CategoryApi(ViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsShopOwner]
    lookup_field = "uid"

    def list(self, request: Request) -> Response:
        categories = Category.objects.filter(
            created_by=request.user, deleted_at__isnull=True
        )
        if request.query_params.get("category_name", None):
            categories = categories.filter(
                name__icontains=request.query_params.get("category_name")
            )

        category_serializer = self.serializer_class(categories, many=True)
        return HttpUtil.success_response(
            data=category_serializer.data, message="success"
        )

    def create(self, request: Request) -> Response:
        try:
            if Category.objects.get(created_by=request.user, name=request.data["name"]):
                return HttpUtil.error_response(
                    message="name with this category already exists!"
                )
        except Category.DoesNotExist:
            category_serializer = self.serializer_class(
                data=request.data, context={"user": request.user}
            )
            if not category_serializer.is_valid():
                return HttpUtil.error_response(category_serializer.errors)

            category_serializer.save(created_by=request.user)
            return HttpUtil.success_response(
                data=category_serializer.data,
                message="created",
                code=status.HTTP_201_CREATED,
            )

    def retrieve(self, request: Request, uid: str = None) -> Response:
        try:
            category = Category.objects.get(
                uid=uid, created_by=request.user, deleted_at__isnull=True
            )
            category_serializer = self.serializer_class(category)
            return HttpUtil.success_response(data=category_serializer.data)
        except Category.DoesNotExist:
            return HttpUtil.error_response(message="category not found.")

    def update(self, request: Request, uid: str = None) -> Response:
        try:
            category = Category.objects.get(
                uid=uid, created_by=request.user, deleted_at__isnull=True
            )
            category_serializer = self.serializer_class(
                category,
                data=request.data,
                context={"user": request.user},
                partial=True,
            )
            if not category_serializer.is_valid():
                return HttpUtil.error_response(category_serializer.errors)
            category_serializer.save()

            return HttpUtil.success_response(data=category_serializer.data)
        except Category.DoesNotExist:
            return HttpUtil.error_response(message="category not found.")

    def delete(self, request: Request, uid: str = None) -> Response:
        try:
            category = Category.objects.get(
                uid=uid, created_by=request.user, deleted_at__isnull=True
            )
            soft_delete(category)
            return HttpUtil.success_response(message="deleted")
        except Category.DoesNotExist:
            return HttpUtil.error_response(message="category not found.")


class InventoryApi(ViewSet):
    serializer_class = InventorySerializer
    permission_classes = [IsShopOwner | IsShopManager | IsShopEmployee]
    lookup_field = "uid"

    def list(self, request: Request) -> Response:
        shop_uid = request.query_params.get("shop_uid")
        inventories = Inventory.objects.filter(
            shop__uid=shop_uid, deleted_at__isnull=True
        )
        shop_serializer = self.serializer_class(inventories, many=True)
        return HttpUtil.success_response(data=shop_serializer.data)

    def create(self, request: Request) -> Response:
        shop = None

        if "created_by" not in request.data:
            request.data["created_by"] = request.user.pk

        if "status" not in request.data:
            request.data["status"] = True

        if "shop_uid" in request.data:
            shop = Shop.objects.get(
                uid=request.data["shop_uid"], deleted_at__isnull=True
            )
            if shop:
                request.data["shop"] = shop.pk

        inventory_serializer = self.serializer_class(data=request.data)
        if not inventory_serializer.is_valid():
            return HttpUtil.error_response(message=inventory_serializer.errors)

        inventory_serializer.save()
        return HttpUtil.success_response(
            message="success", code=status.HTTP_201_CREATED
        )

    def retrieve(self, request: Request, uid: str = None) -> Response:
        try:
            inventory = Inventory.objects.get(uid=uid, deleted_at__isnull=True)
            inventory_serializer = self.serializer_class(inventory, many=False)
            return HttpUtil.success_response(data=inventory_serializer.data)

        except Inventory.DoesNotExist:
            return HttpUtil.error_response("Inventory doesn't found!")

    def update(self, request: Request, uid: str = None) -> Response:
        try:
            inventory = Inventory.objects.get(uid=uid, deleted_at__isnull=True)
            if "name" not in request.data:
                request.data["name"] = inventory.name

            if "created_by" not in request.data:
                request.data["created_by"] = inventory.created_by.id

            if "shop" not in request.data:
                request.data["shop"] = inventory.shop.id

            inventory_serializer = self.serializer_class(inventory, data=request.data)
            if not inventory_serializer.is_valid():
                return HttpUtil.error_response(message=inventory_serializer.errors)

            inventory_serializer.save(updated_by=request.user)
            return HttpUtil.success_response(
                data=inventory_serializer.data, message="updated"
            )

        except Inventory.DoesNotExist:
            return HttpUtil.error_response("Inventory doesn't found!")

    def delete(self, request: Request, uid: str = None) -> Response:
        try:
            inventory = Inventory.objects.get(uid=uid, deleted_at__isnull=True)
            inventory.delete()
            return HttpUtil.success_response(message="deleted")

        except Inventory.DoesNotExist:
            return HttpUtil.error_response("Inventory doesn't found!")


class StockEntryApi(ViewSet):
    serializer_class = InventorySerializer
    permission_classes = [IsShopOwner | IsShopManager | IsShopEmployee]
    lookup_field = "uid"

    def update(self, request: Request, uid: str = None) -> Response:
        try:
            inventory = Inventory.objects.get(
                uid=uid,
                deleted_at__isnull=True,
                shop__uid=request.query_params.get("shop_uid"),
            )

            if "total_stock" not in request.data:
                return HttpUtil.error_response(message="stock qty missing.")

            request.data["total_stock"] = decimal.Decimal(
                request.data["total_stock"]
            ) + decimal.Decimal(inventory.total_stock)

            # Ensure required fields have default values
            data = request.data.copy()
            data.setdefault("name", inventory.name)
            data.setdefault(
                "created_by", inventory.created_by.id if inventory.created_by else None
            )
            data.setdefault("shop", inventory.shop.id if inventory.shop else None)

            # Update the inventory item
            inventory_serializer = self.serializer_class(inventory, data=data)
            if not inventory_serializer.is_valid():
                return HttpUtil.error_response(message=inventory_serializer.errors)

            inventory_serializer.save()
            return HttpUtil.success_response(message="Inventory updated successfully.")

        except Inventory.DoesNotExist:
            return HttpUtil.error_response(message="inventory item not found!")


class StockOutApi(ViewSet):
    serializer_class = InventorySerializer
    permission_classes = [IsShopOwner | IsShopManager | IsShopEmployee]
    lookup_field = "uid"

    def update(self, request: Request, uid: str = None) -> Response:
        try:
            inventory = Inventory.objects.get(
                uid=uid,
                deleted_at__isnull=True,
                shop__uid=request.query_params.get("shop_uid"),
            )

            if "total_stock" not in request.data:
                return HttpUtil.error_response(message="stock qty missing.")

            if decimal.Decimal(request.data["total_stock"]) > decimal.Decimal(
                inventory.total_stock
            ):
                return HttpUtil.error_response(message="you don't have enough stock")

            request.data["total_stock"] = decimal.Decimal(
                inventory.total_stock
            ) - decimal.Decimal(request.data["total_stock"])

            # Ensure required fields have default values
            data = request.data.copy()
            data.setdefault("name", inventory.name)
            data.setdefault(
                "created_by", inventory.created_by.id if inventory.created_by else None
            )
            data.setdefault("shop", inventory.shop.id if inventory.shop else None)

            # Update the inventory item
            inventory_serializer = self.serializer_class(inventory, data=data)
            if not inventory_serializer.is_valid():
                return HttpUtil.error_response(message=inventory_serializer.errors)

            inventory_serializer.save()
            return HttpUtil.success_response(message="Inventory updated successfully.")

        except Inventory.DoesNotExist:
            return HttpUtil.error_response(message="inventory item not found!")


class SaleApi(ViewSet):
    permission_classes = [IsShopOwner | IsShopEmployee | IsShopManager]
    sale_serializer_class = SaleSerializer
    sale_detail_serializer = SaleDetailSerializer
    lookup_field = "uid"

    def list(self, request: Request) -> Response:
        shop_uid = request.query_params.get("shop_uid", None)
        if not shop_uid:
            return HttpUtil.error_response(message="shop missing")

        sales = Sale.objects.filter(shop__uid=shop_uid, deleted_at__isnull=True)
        sale_serializer = self.sale_serializer_class(sales, many=True)
        return HttpUtil.success_response(data=sale_serializer.data)

    def create(self, request: Request) -> Response:
        payload = request.data
        sale_serializer = self.sale_serializer_class(data=payload)
        if not sale_serializer.is_valid():
            return HttpUtil.error_response(message=sale_serializer.errors)
        sale_serializer.save()
        return HttpUtil.success_response(
            message="sale created", code=status.HTTP_201_CREATED
        )

    def retrieve(self, request: Request, uid: str) -> Response:
        try:
            sale = Sale.objects.get(uid=uid, deleted_at__isnull=True)
        except Sale.DoesNotExist:
            return HttpUtil.error_response(message="sale doesn't exists!")

        sale_serializer = self.sale_serializer_class(sale, many=False)
        return HttpUtil.success_response(data=sale_serializer.data)

    def delete(self, request: Request, uid: str) -> Response:
        try:
            sale = Sale.objects.get(uid=uid, deleted_at__isnull=True)
        except Sale.DoesNotExist:
            return HttpUtil.error_response(message="Sale not found!")

        """
            1. from sale details, adjust the quantity to inventory
            2. delete sale details
            3. delete sale
        """
        for sale_detail in SaleDetail.objects.filter(sale=sale):
            try:
                inventory = Inventory.objects.get(id=sale_detail.inventory_id)
                inventory.total_stock = inventory.total_stock + sale_detail.qty
                inventory.save()
            except Inventory.DoesNotExist:
                pass

        sale_detail.delete()
        sale.delete()
        return HttpUtil.success_response(message="sale deleted and stock rebased.")


class CustomerApi(ViewSet):
    permission_classes = [IsShopOwner | IsShopManager | IsShopEmployee]
    serializer_class = CustomerSerializer
    lookup_field = "uid"

    def check_shop(self, shop_uid: Union[str, None]) -> Union[Shop, None]:
        if shop_uid is None:
            return None

        try:
            shop = Shop.objects.get(uid=shop_uid, deleted_at__isnull=True)
        except Shop.DoesNotExist:
            return None

        return shop

    def check_customer(self, shop, customer_uid):
        if customer_uid is None:
            return None

        try:
            customer = Customer.objects.get(
                shop=shop, uid=customer_uid, deleted_at__isnull=True
            )
        except Customer.DoesNotExist:
            return None

        return customer

    def list(self, request: Request) -> Response:
        shop_uid = request.query_params.get("shop_uid", None)
        shop = self.check_shop(shop_uid)
        if shop is None:
            return HttpUtil.error_response(message="Shop Not Defined!")

        customers = Customer.objects.filter(shop__uid=shop.uid, deleted_at__isnull=True)
        customer_serializer = self.serializer_class(customers, many=True)
        return HttpUtil.success_response(data=customer_serializer.data)

    def create(self, request: Request) -> Response:
        payload = request.data
        shop_uid = request.query_params.get("shop_uid", None)
        shop = self.check_shop(shop_uid)
        if shop is None:
            return HttpUtil.error_response(message="Shop Not Defined!")
        customer_serializer = self.serializer_class(data=payload)
        if not customer_serializer.is_valid():
            return HttpUtil.error_response(message=customer_serializer.errors)

        customer_serializer.save(
            shop=shop, deleted_at__isnull=True, created_by=request.user
        )
        return HttpUtil.success_response(
            message="Customer Created", code=status.HTTP_201_CREATED
        )

    def get(self, request: Request, uid: str) -> Response:
        shop_uid = request.query_params.get("shop_uid", None)
        shop = self.check_shop(shop_uid)
        customer = self.check_customer(shop, uid)
        if (shop and customer) is None:
            return HttpUtil.error_response(message="Shop Not Defined!")
        customer_serializer = self.serializer_class(customer, many=False)
        return HttpUtil.success_response(data=customer_serializer.data)

    def update(self, request: Request, uid: str) -> Response:
        shop_uid = request.query_params.get("shop_uid", None)
        shop = self.check_shop(shop_uid)
        customer = self.check_customer(shop, uid)
        if (shop and customer) is None:
            return HttpUtil.error_response(message="Shop Not Defined!")

        customer_serializer = self.serializer_class(
            customer, data=request.data, partial=True
        )
        if not customer_serializer.is_valid():
            return HttpUtil.error_response(message=customer_serializer.errors)

        customer_serializer.save()
        return HttpUtil.success_response(
            data=customer_serializer.data, message="Customer Updated"
        )

    def delete(self, request: Request, uid: str) -> Response:
        shop_uid = request.query_params.get("shop_uid", None)
        shop = self.check_shop(shop_uid)
        customer = self.check_customer(shop, uid)
        if (shop and customer) is None:
            return HttpUtil.error_response(message="Shop Not Defined!")
        customer.delete()
        return HttpUtil.success_response(message="Customer Deleted")


class PayableSaleApi(ViewSet):
    permission_classes = [IsShopOwner | IsShopManager | IsShopEmployee]
    serializer_class = SaleSerializer

    def list(self, request: Request) -> Response:
        shop_uid = request.query_params.get("shop_uid", None)
        filter_query = {
            "start_date": request.query_params.get("start_date", None),
            "end_date": request.query_params.get("end_date", None),
        }
        if shop_uid is None:
            return HttpUtil.error_response(message="Shop Not Found!")

        payable_sales = Sale.objects.filter(
            shop__uid=shop_uid, deleted_at__isnull=True, is_paid=False, **filter_query
        )
        payable_serializer = self.serializer_class(payable_sales, many=True)
        return HttpUtil.success_response(data=payable_serializer.data)
