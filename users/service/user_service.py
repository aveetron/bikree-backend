from datetime import datetime

import jwt
from django.conf import settings

from users.models import User


class UserService:
    """
    User Service
    It will be used to interact with user
    """

    Instance = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not cls.Instance:
            cls.Instance = super(UserService, cls).__new__(cls, *args, **kwargs)
        return cls.Instance

    @staticmethod
    def create_verification_token(user: User):
        """
        Create verification token
        :param user:
        :return:
        """
        try:
            return jwt.encode(
                {
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(days=365),
                    "iat": datetime.datetime.utcnow(),
                    "nbf": datetime.datetime.utcnow(),
                    "email": user.email,
                    "user_guid": user.guid.hex,
                },
                settings.SECRET_KEY,
                algorithm="HS256",
            )
        except Exception as e:
            return None

    @staticmethod
    def verify_email_verification_token(token: str):
        """
        Verify email verification token
        :param token:
        :return:
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return "Token expired"
        except jwt.exceptions.DecodeError:
            return "Invalid token"
        except jwt.InvalidTokenError:
            return "Invalid token"
        except Exception as e:
            return "Invalid token"

    @staticmethod
    def activate_user(user: User):
        """
        Activate user
        :param user:
        :return:
        """
        try:
            user.is_active = True
            user.save()
            return user
        except Exception as e:
            return None

    @staticmethod
    def get_user_by_phone(phone: str):
        """
        Get user by email
        :param phone:
        :return:
        """
        try:
            user = User.objects.get(phone=phone)
            return user
        except User.DoesNotExist:
            return None
        except Exception as e:
            return None

    @staticmethod
    def get_user_by_guid(guid: str):
        """
        Get user by guid
        :param guid:
        :return:
        """
        try:
            user = User.objects.get(guid=guid)
            return user
        except User.DoesNotExist:
            return None
        except Exception as e:
            return None
