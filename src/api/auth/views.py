import json

from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.core.exceptions import PermissionDenied
from django.views import View

from api.utils.errors import error_response, handler403
from api.internal.models.employee import Employee
from .serializers import serialize_auth


def get_absolute_url(request):
    scheme = request.scheme
    host = request.META['HTTP_HOST']

    return f'{scheme}://{host}'


class AuthenticatedView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user:
            return handler403(request, PermissionDenied)

        return super().dispatch(request, *args, **kwargs)


class AdminAuthenticatedView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return handler403(request, PermissionDenied)

        return super().dispatch(request, *args, **kwargs)


class LoginView(View):
    def post(self, request):
        data = json.loads(request.body or '{}')
        username = data.get('username', '').lower()
        password = data.get('password', None)
        if username and password:
            try:
                user = Employee.objects.get(username=username)
                if not check_password(password, user.password):
                    return error_response('auth', 'Incorrect password')
                return JsonResponse(serialize_auth(user), status=200)
            except Employee.DoesNotExist:
                return error_response('auth', 'Unable to login with the provided credentials')
        else:
            return error_response('auth', 'Please enter username and password')
