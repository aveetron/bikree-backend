from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)

from core.routes.config import config_router
from core.routes.customer import customer_router
from core.routes.inventory import inventory_router
from core.routes.sale import sale_router
from core.routes.shop import shop_router
from core.routes.users import users_router
from core.routes.category import category_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/users/', include(users_router.urls)),
    path('api/v1/config/', include(config_router.urls)),
    path('api/v1/shop/', include(shop_router.urls)),
    path('api/v1/category/', include(category_router.urls)),
    path('api/v1/inventory/', include(inventory_router.urls)),
    path('api/v1/sale/', include(sale_router.urls)),
    path('api/v1/customer/', include(customer_router.urls)),
]