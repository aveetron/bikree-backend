from rest_framework import status
from rest_framework.viewsets import ViewSet

from core.http_utils import HttpUtil
from core.permissions import IsShopOwner
from shop.models import Shop
from shop.serializers import ShopSerializer


class ShopApi(ViewSet):
    serializer_class = ShopSerializer
    permission_classes = [IsShopOwner]
    lookup_field = "guid"

    def list(self, request):
        shops = Shop.objects.filter(
            owner=request.user,
            status=True
        )
        shop_serializer = self.serializer_class(
            shops, many=True
        )
        return HttpUtil.success_response(
            data=shop_serializer.data,
            message="success"
        )

    def create(self, request):
        shop_serializer = self.serializer_class(
            data=request.data,
            context={"user": request.user}
        )
        if not shop_serializer.is_valid():
            return HttpUtil.error_response(
                shop_serializer.errors
            )
        shop_serializer.save(
            owner=request.user
        )
        return HttpUtil.success_response(
            data=shop_serializer.data,
            message="created",
            code=status.HTTP_201_CREATED
        )

    def retrieve(self, request, guid):
        try:
            shop = Shop.objects.get(
                guid=guid,
                owner=request.user,
                status=True
            )
            shop_serializer = ShopSerializer(shop)
            return HttpUtil.success_response(
                data=shop_serializer.data
            )
        except Shop.DoesNotExist:
            return HttpUtil.error_response(
                message="shop not found."
            )

    def update(self, request, guid):
        try:
            shop = Shop.objects.get(
                guid=guid,
                owner=request.user,
                status=True
            )
            shop_serializer = ShopSerializer(
                shop, data=request.data,
                context={"user": request.user}
            )
            if not shop_serializer.is_valid():
                return HttpUtil.error_response(
                    shop_serializer.errors
                )
            shop_serializer.save()

            return HttpUtil.success_response(
                data=shop_serializer.data
            )
        except Shop.DoesNotExist:
            return HttpUtil.error_response(
                message="shop not found."
            )

    def delete(self, request, guid):
        try:
            shop = Shop.objects.get(
                guid=guid,
                owner=request.user,
                status=True
            )
            shop.delete()
            return HttpUtil.success_response(
                message="deleted"
            )
        except Shop.DoesNotExist:
            return HttpUtil.error_response(
                message="shop not found."
            )