from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class CreateUserRateThrottle(AnonRateThrottle):
    scope = "create_user"


class UpdatePasswordRateThrottle(UserRateThrottle):
    scope = "update_password"
