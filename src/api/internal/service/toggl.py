from decimal import Decimal

from django.db.models import Sum
from api.internal.models.toggl import TogglRecord
from toggl.TogglPy import Toggl as TogglBase


ME_ENDPOINT = 'https://api.track.toggl.com/api/v8/me'


class Toggl(TogglBase):
    def getMe(self):
        return self.request(ME_ENDPOINT)

    
class TogglService:
    def __init__(self):
        pass

    @staticmethod
    def filter_by_employee(employee_id):
        return TogglRecord.objects.filter(employee__id=employee_id).select_related('project')

    @staticmethod
    def filter_by_kwargs(**kwargs):
        return TogglRecord.objects.filter(**kwargs)

    @staticmethod
    def count_hours_by_toggl_records(records) -> float:
        return (records.aggregate(Sum('seconds'))['seconds__sum'] or 0) / 3600

    @staticmethod
    def filter_records_by_date(records, since=None, until=None):
        kwargs = {}
        if since:
            kwargs['start__date__gte'] = since
        if until:
            kwargs['start__date__lte'] = until

        return records.filter(**kwargs)

    @staticmethod
    def get_toggl_records_by_client(client, date_range):
        kwargs = {}
        if 'date__lte' in date_range.keys():
            kwargs['start__date__lte'] = date_range['date__lte'].year

        if 'date__gte' in date_range.keys():
            kwargs['start__date__gte'] = date_range['date__gte'].year

        return TogglRecord.objects.filter(project__client=client, **kwargs)

    def toggl_expense_by_client(self, client, date_range, currency):
        records = self.get_toggl_records_by_client(client, date_range)
        expense = 0
        for record in records:
            if record.employee.currency == currency:
                expense += record.seconds / Decimal(3600) * (record.rate / Decimal(160))

        return expense
