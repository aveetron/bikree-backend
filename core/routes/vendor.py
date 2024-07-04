from rest_framework.routers import DefaultRouter

from shop.views import VendorApi

vendor_router = DefaultRouter()

vendor_router.register("", VendorApi, basename="vendor")