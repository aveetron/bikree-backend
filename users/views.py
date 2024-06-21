from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from core.http_utils import HttpUtil
from users.serializers import UserSerializer


class RegistrationApi(ViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request: Request, format=None) -> Response:
        payload = request.data
        if not payload["phone"]:
            return HttpUtil.error_response("Phone is required")
        user_serializer = self.serializer_class(
            data=payload
        )
        if user_serializer.is_valid():
            """
            Register a new user
            """
            user_serializer.save(is_active=True)
            return HttpUtil.success_response(
                "user created successfully.",
                {},
                status.HTTP_201_CREATED,
            )
        else:
            return HttpUtil.error_response(user_serializer.errors)
