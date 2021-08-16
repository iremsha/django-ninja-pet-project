import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from ninja.security import HttpBearer, APIKeyHeader


class HTTPJWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
            user = get_user_model().objects.get(id=payload['id'])
            request.user = user
        except:
            return None

        return token


class HTTPAdminJWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
            user = get_user_model().objects.get(id=payload['id'])
        except:
            return None

        if not user.is_superuser:
            return None
        request.user = user

        return token


class ApiKeyAuth(APIKeyHeader):
    param_name: str = "X-API-KEY"

    def authenticate(self, request, key):
        if key == settings.SECRET_KEY:
            return key
