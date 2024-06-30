from rest_framework import status, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from config.models import Uom
from config.serializers import UomSerializer
from core.permissions import IsAdmin, IsBusinessAnalyst
from core.http_utils import HttpUtil


class UomApi(ViewSet):
    serializer_class = UomSerializer
    permission_classes = [IsAdmin | IsBusinessAnalyst]
    lookup_field = "uid"

    def get_permissions(self) -> list:
        if self.action == "list":
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def list(self, request: Request) -> Response:
        """
        any authenticated person can view uom lists
        :param request: None
        :return: uoms
        """
        uoms = Uom.objects.filter(deleted_at__isnull=False)
        uom_serializer = self.serializer_class(
            uoms,
            many=True
        )
        return HttpUtil.success_response(
            data=uom_serializer.data
        )

    def create(self, request: Request) -> Response:
        uom_serializer = self.serializer_class(
            data=request.data
        )
        if not uom_serializer.is_valid():
            return HttpUtil.error_response(
                uom_serializer.errors
            )
        uom_serializer.save()
        return HttpUtil.success_response(
            data=uom_serializer.data,
            code=status.HTTP_201_CREATED,
            message="created"
        )

    def retrieve(self, request: Request, uid: str = None) -> Response:
        try:
            uom = Uom.objects.get(uid=uid)
            uom_serializer = self.serializer_class(
                uom, many=False
            )
            return HttpUtil.success_response(
                data=uom_serializer.data
            )
        except Uom.DoesNotExist:
            return HttpUtil.error_response(
                message="uom not found!"
            )

    def update(self, request: Request, uid: str = None) -> Response:
        try:
            uom = Uom.objects.get(uid=uid)
            uom_serializer = self.serializer_class(
                uom, data=request.data
            )
            if not uom_serializer.is_valid():
                return HttpUtil.error_response(
                    uom_serializer.errors
                )
            uom_serializer.save()
            return HttpUtil.success_response(
                data=uom_serializer.data,
                message="updated."
            )
        except Uom.DoesNotExist:
            return HttpUtil.error_response(
                message="uom not found!"
            )

    def delete(self, request: Request, uid: str = None) -> Response:
        try:
            uom = Uom.objects.get(uid=uid)
            uom.delete()
            return HttpUtil.success_response(
                message="uom deleted."
            )
        except Uom.DoesNotExist:
            return HttpUtil.error_response(
                message="uom not found!"
            )