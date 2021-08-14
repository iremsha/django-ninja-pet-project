from ninja import Schema
from typing import Optional, List
from uuid import UUID
from django.conf import settings
from api.internal.models.employee import EmployeePhoto


def get_gender(name):
    if name is None or name == str():
        return 'male'
    if name == 'Никита' or name == 'Лёва' or name == 'Илья':
        return 'male'
    if name[-1] in ['а', 'я', 'и', 'ю'] or name == 'Любовь':
        return 'female'
    return 'male'


def get_path_to_avatar(employee):
    if employee.main_photo:
        avatar = EmployeePhoto.objects.get(employee=employee).main_photo_300x300.url
        avatar = avatar[:avatar.find('AWSA')-1]
    elif employee.personal_photo:
        avatar = EmployeePhoto.objects.get(employee=employee).personal_photo_300x300.url
        avatar = avatar[:avatar.find('AWSA')-1]
    else:
        gender = get_gender(employee.first_name)
        avatar = f'{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/images/{gender}300x300.png'

    return avatar


class EmployeePaymentMethodOut(Schema):
    id: int
    name: Optional[str]
    category: Optional[str]
    currency: Optional[str]
    card_number: Optional[str]


class EmployeePaymentMethodsOut(Schema):
    payment_methods: Optional[List[EmployeePaymentMethodOut]]


class EmployeeWithPaymentMethodsOut(Schema):
    id: UUID
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    work_status: Optional[str]
    avatar: Optional[str]
    currency: Optional[str]
    payment_methods: Optional[List[EmployeePaymentMethodOut]]


class DepartmentOut(Schema):
    id: int
    name: str


class DepartmentListOut(Schema):
    count: int
    items: List[DepartmentOut]


class EmployeeShortOut(Schema):
    id: UUID
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    work_status: Optional[str]
    avatar: Optional[str]
    currency: Optional[str]
    department: Optional[DepartmentOut]


class EmployeeShortListOut(Schema):
    count: int
    employees: Optional[List[EmployeeShortOut]]


class EmployeeTrackedHoursOut(Schema):
    hours_per_period: float
    hours_by_projects: str
