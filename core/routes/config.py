from rest_framework.routers import DefaultRouter

from config.views import UomApi

config_router = DefaultRouter()


config_router.register("uom", UomApi, basename="uom")