from rest_framework.routers import DefaultRouter

from shop.views import SaleApi

sale_router = DefaultRouter()

sale_router.register("", SaleApi, basename="sale")
