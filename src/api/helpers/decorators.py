import functools
import json
from .errors import not_valid_response, error_response
from django import forms


def validate_form(form_cls):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, request, *args, **kwargs):
            data = json.loads(request.body or '{}')
            form = form_cls(data, request=request)
            if not form.is_valid():
                return not_valid_response(form.errors)
            return func(self, request, *args, **kwargs, form_data=form.cleaned_data)
        return wrapper
    return decorator


def get_model_obj_by_id(model_cls):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, request, id):
            try:
                obj = model_cls.objects.get(id=id)
            except:
                return error_response('notfound', 'Id not found', 404)
            return func(self, request, id, obj=obj)
        return wrapper
    return decorator
