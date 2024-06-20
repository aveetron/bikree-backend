from rest_framework.routers import DefaultRouter

from shop.views import InventoryApi, StockEntryApi

inventory_router = DefaultRouter()

inventory_router.register("", InventoryApi, basename="inventory")
inventory_router.register("stock-entry", StockEntryApi, basename="stock-entry")