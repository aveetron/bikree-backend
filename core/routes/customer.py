from rest_framework.routers import DefaultRouter

from shop.views import CustomerApi

customer_router = DefaultRouter()

customer_router.register("", CustomerApi, basename="customer")
