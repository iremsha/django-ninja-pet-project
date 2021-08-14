import jwt
from api.internal.transport.rest.employee.responses import get_path_to_avatar
from django.conf import settings


def serialize_auth(user):
    return dict(
        token=jwt.encode({'id': str(user.pk)}, settings.JWT_SECRET, algorithm='HS256').decode('utf-8'),
        user=serialize_user(user),
    )


def serialize_user(user):
    avatar = get_path_to_avatar(user)

    return dict(
        id=user.pk,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        avatar=avatar,
    )
