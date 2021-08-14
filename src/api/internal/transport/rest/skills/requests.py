from ninja import Schema
from typing import Optional, List

from api.internal.transport.rest.skills.responses import SkillScoreIn


class SkillListQuery(Schema):
    section: int
    department: Optional[int]
    limit: int = 20
    offset: int = 0


class SkillScoreListIn(Schema):
    items: List[SkillScoreIn]
