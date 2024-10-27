from rest_framework.routers import DefaultRouter

from sales_representative.views import OrderApi

sr_router = DefaultRouter()


sr_router.register("orders", OrderApi, basename="sr-order")
