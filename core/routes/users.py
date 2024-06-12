from rest_framework.routers import DefaultRouter

from users.views import RegistrationApi

users_router = DefaultRouter()


users_router.register("registration", RegistrationApi, basename="registration")