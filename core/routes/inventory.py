from rest_framework.routers import DefaultRouter

from shop.views import InventoryApi

inventory_router = DefaultRouter()

inventory_router.register("", InventoryApi, basename="inventory")