import sys
import traceback
from enum import Enum
from django.http import JsonResponse


class Errors(Enum):
    auth_password = 'Incorrect password'
    auth_no_login_or_password = 'Please enter username and password'
    auth_login = 'Unable to login with the provided credentials'
    validation_failed = 'Ошибка валидации'
    toggle_validation_failed = 'Не найдены ключи проектов.'
    notfound = 'Not found.'
    forbidden = 'You are not authorized to make this request.'
    unknown = 'Something went wrong. Please try again later.'
    project_amount = 'Amount of incomes is incorrect'
    employee = 'Employee not found'
    equipment = 'Equipment not found'
    equipment_occupied = 'Equipment is occupied by other employee'


def error_response(code, message, status=400):
    return JsonResponse({
        'errors': [{
            'code': code,
            'message': message,
        }]
    }, status=status)


def not_valid_response(errors, status=400):
    return JsonResponse({
        'errors': [{
            'code': Errors.validation_failed.name,
            'message': Errors.validation_failed.value,
            'fields': errors
        }]
    }, status=status)


def toggl_projects_error_response(errors, status=400):
    return JsonResponse({
        'errors': [{
            'code': Errors.toggle_validation_failed.name,
            'message': Errors.toggle_validation_failed.value,
            'keys': errors
        }]
    }, status=status)


def print_traceback():
    type, value, tb = sys.exc_info()
    print(traceback.format_exception(type, value, tb))


def handler500(request):
    print_traceback()
    type, value, tb = sys.exc_info()
    if type is APIException:
        return value.reason

    return error_response(str(type), str(value), status=500)


def handler400(request, exception):
    return error_response(Errors.unknown.name, Errors.unknown.value, status=400)


def handler404(request, exception):
    print_traceback()
    return error_response(Errors.notfound.name, Errors.notfound.value, status=404)


def handler403(request, exception):
    print_traceback()
    return error_response(Errors.forbidden.name, Errors.forbidden.value, status=403)


class APIException(Exception):
    def __init__(self, status, reason):
        super().__init__()
        self.status = status
        self.reason = reason
