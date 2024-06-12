from rest_framework.exceptions import APIException


class HttpException(APIException):
    """
    A base class for all HTTP exceptions.
    """

    status_code = None
    default_detail = None
    default_code = None

    def __init__(self, message: str, code: int, data: dict = None):
        _detail = {
            "data": data or {},
            "response_message": message,
            "response_code": code,
        }
        super().__init__(_detail, code)
        self.status_code = code
        self.default_detail = _detail
        self.default_code = code


class UserNotFoundException(HttpException):
    def __init__(self):
        super().__init__("User not found", 404)


class UserAlreadyExistsException(HttpException):
    def __init__(self):
        super().__init__("User already exists", 409)
