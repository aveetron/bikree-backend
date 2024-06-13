from rest_framework.routers import DefaultRouter

from shop.views import ShopApi

shop_router = DefaultRouter()


shop_router.register("", ShopApi, basename="shop")