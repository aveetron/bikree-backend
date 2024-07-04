from typing import Union

from core.http_utils import HttpUtil
from shop.models import Customer, Shop, Vendor


class BaseHelper:

    def __init__(self):
        pass


class UserHandler(BaseHelper):

    def check_shop_wise_customer(
        shop: Shop, customer_uid: Union[str, None]
    ) -> Union[Customer, HttpUtil]:
        if customer_uid is None:
            return HttpUtil.error_response(message="Customer Not Defined!")

        try:
            customer = Customer.objects.get(
                shop=shop, uid=customer_uid, deleted_at__isnull=True
            )
        except Customer.DoesNotExist:
            return HttpUtil.error_response(message="Customer Not Defined!")

        return customer

    def check_shop_wise_vendor(
        shop: Shop, vendor_uid: Union[str, None]
    ) -> Union[Vendor, HttpUtil]:
        if vendor_uid is None:
            return HttpUtil.error_response(message="Vendor Not Defined")

        try:
            vendor = Vendor.objects.get(
                shop=shop, uid=vendor_uid, deleted_at__isnull=True
            )
        except Vendor.DoesNotExist:
            return HttpUtil.error_response(message="Vendor Not Defined")

        return vendor


class ShopHandler(BaseHelper):

    @staticmethod
    def check_shop(shop_uid: Union[str, None]) -> Union[Shop, HttpUtil]:
        if shop_uid is None:
            return HttpUtil.error_response(message="Shop Not Defined!")

        try:
            shop = Shop.objects.get(uid=shop_uid, deleted_at__isnull=True)
        except Shop.DoesNotExist:
            return HttpUtil.error_response(message="Shop Not Defined!")

        return shop
