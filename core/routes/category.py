from rest_framework.routers import DefaultRouter

from shop.views import CategoryApi

category_router = DefaultRouter()

category_router.register("", CategoryApi, basename="category")
