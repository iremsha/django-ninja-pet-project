from uuid import UUID
from ninja import Schema
from typing import List


class SkillScoreDTO(Schema):
    score: int
    skill: int
    employee: UUID


class AddSkillScoreList(Schema):
    items: List[SkillScoreDTO]
