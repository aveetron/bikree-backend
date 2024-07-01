from typing import Union

from shop.models import Customer, Shop


class BaseHelper:

    def __init__(self):
        pass


class UserHandler(BaseHelper):

    def check_shop_wise_customer(
        self, shop: Shop, customer_uid: str
    ) -> Union[Customer, None]:
        if customer_uid is None:
            return None

        try:
            customer = Customer.objects.get(
                shop=shop, uid=customer_uid, deleted_at__isnull=True
            )
        except Customer.DoesNotExist:
            return None

        return customer


class ShopHandler(BaseHelper):

    @staticmethod
    def check_shop(self, shop_uid: Union[str, None]) -> Union[Shop, None]:
        if shop_uid is None:
            return None

        try:
            shop = Shop.objects.get(uid=shop_uid, deleted_at__isnull=True)
        except Shop.DoesNotExist:
            return None

        return shop
