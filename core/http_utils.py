from rest_framework.response import Response


class HttpUtil:
    def __init__(self):
        pass

    @staticmethod
    def success_response(message: str = None, data: dict = None, code: int = 200):
        return Response(
            {
                "data": data or {},
                "response_message": message,
                "response_code": code,
            },
            status=code,
        )

    @staticmethod
    def error_response(message: str = None, data: dict = None, code: int = 400):
        return Response(
            {
                "data": data or {},
                "response_message": message,
                "response_code": code,
            },
            status=code,
        )
