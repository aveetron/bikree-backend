from abc import abstractmethod
from typing import Union, List

from rest_framework import permissions
from rest_framework.request import Request

from users.models import User, Role


class BaseUserPermission(permissions.BasePermission):
    @abstractmethod
    def get_role(self) -> Union[str, List[str]]:
        raise NotImplementedError()

    def find_user(self, user_id: int):
        if isinstance(self.get_role(), str):
            roles = [self.get_role()]
        else:
            roles = self.get_role()
        return User.objects.get(
            id=user_id,
            role__name__in=roles,
            is_active=True,
        )

    def has_permission(self, request: Request, view: object) -> bool:
        if request.user and request.user.id:
            try:
                request.user = self.find_user(request.user.id)
            except User.DoesNotExist:
                return False
            return True
        return False


class IsAdmin(BaseUserPermission):

    def get_role(self) -> str:
        return Role.ADMIN


class IsBusinessAnalyst(BaseUserPermission):

    def get_role(self) -> str:
        return Role.BUSINESS_ANALYST


class IsAdminOrBusinessAnalyst(BaseUserPermission):

    def get_role(self) -> list[str]:
        return [Role.ADMIN, Role.BUSINESS_ANALYST]


class IsShopOwner(BaseUserPermission):

    def get_role(self) -> str:
        return Role.SHOP_OWNER


class IsShopManager(BaseUserPermission):

    def get_role(self) -> str:
        return Role.SHOP_MANAGER


class IsShopEmployee(BaseUserPermission):

    def get_role(self) -> str:
        return Role.SHOP_EMPLOYEE


class IsShopOwnerOrManager(BaseUserPermission):

    def get_role(self) -> list[str]:
        return [Role.SHOP_OWNER, Role.SHOP_MANAGER]


class IsShopManagerOrEmployee(BaseUserPermission):

    def get_role(self) -> list[str]:
        return [Role.SHOP_MANAGER, Role.SHOP_EMPLOYEE]


class IsShopOwnerOrEmployee(BaseUserPermission):

    def get_role(self) -> list[str]:
        return [Role.SHOP_OWNER, Role.SHOP_EMPLOYEE]
