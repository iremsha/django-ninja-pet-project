from datetime import timedelta
from celery.schedules import crontab


CELERYBEAT_SCHEDULE = {
   'DEADLINE': {
     'task': 'DEADLINE',
     'schedule': crontab(hour=10, minute=21),
  },
}