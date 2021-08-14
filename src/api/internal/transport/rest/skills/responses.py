from typing import List, Optional
from uuid import UUID

from ninja import Schema
from ninja.orm import create_schema

from api.internal.models.skills import Skill, SkillScore

SkillOut = create_schema(Skill, depth=1)
SkillScoreOut = create_schema(SkillScore)


class EditSkillIn(Schema):
    name: Optional[str]
    description: Optional[str] = None
    section: Optional[int]
    group: Optional[int]
    departments: Optional[List[int]]


class SkillIn(Schema):
    name: str
    description: Optional[str] = None
    section: int
    group: int
    departments: List[int]


class SkillListOut(Schema):
    count: int
    items: List[SkillOut]


class SkillScoreListOut(Schema):
    count: int
    items: List[SkillScoreOut]


class SkillScoreIn(Schema):
    score: int
    skill: int
    employee: UUID


class SkillSectionOut(Schema):
    id: int
    name: str


class SkillSectionListOut(Schema):
    count: int
    items: List[SkillSectionOut]


class SkillGroupOut(Schema):
    id: int
    name: str


class SkillGroupListOut(Schema):
    count: int
    items: List[SkillGroupOut]
