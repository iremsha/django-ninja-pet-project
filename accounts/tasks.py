# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.task import periodic_task
from celery.schedules import crontab
from .models import Ad


@shared_task
def hold_deduction():
    result = Ad.objects.all()
    for person in result:
        person.save()
        if person.status:
            person.balance -= person.hold
            person.hold = 0
            person.save()
