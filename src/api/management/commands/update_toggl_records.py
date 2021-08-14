import logging

from django.core.management.base import BaseCommand
from api.internal.models.employee import Employee
from api.internal.models.toggl import TogglRecord
from api.employee_api.toggl.views import TogglView, get_str_month
import time


class Command(BaseCommand):
    def handle(self, *args, **options):
        TogglRecord.objects.all().delete()
        count = Employee.objects.count()
        for id, employee in zip(range(count), Employee.objects.all()):
            logging.info(f'{employee} ({id + 1}/{count})')
            for month in range(1, 13):
                month = get_str_month(month)
                TogglView.create_toggl_records(employee, '2020', month)
                time.sleep(2)
                TogglView.create_toggl_records(employee, '2021', month)
                time.sleep(2)
                logging.info(f'{month} completed')
