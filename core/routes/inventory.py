from rest_framework.routers import DefaultRouter

from shop.views import InventoryApi, StockEntryApi, StockOutApi

inventory_router = DefaultRouter()

inventory_router.register("", InventoryApi, basename="inventory")
inventory_router.register("stock-entry", StockEntryApi, basename="stock-entry")
inventory_router.register("stock-out", StockOutApi, basename="stock-out")
