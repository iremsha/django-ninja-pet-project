from typing import List

from ninja import Schema
from ninja.orm import create_schema

from api.internal.models.project import Project

ProjectOut = create_schema(Project, depth=3)


class ProjectShortOut(Schema):
    id: int
    key: str
    name: str


class ProjectListOut(Schema):
    count: int
    items: List[ProjectOut]


class ProjectHoursOut(Schema):
    hours_per_period: float
    employee_hours: float
