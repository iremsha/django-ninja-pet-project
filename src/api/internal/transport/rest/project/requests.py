from typing import Optional

from ninja import Schema
from datetime import date


class ProjectHoursIn(Schema):
    since: Optional[date] = None
    until: Optional[date] = None
