from uuid import UUID
from ninja import Schema
from typing import List


class PetScoreDTO(Schema):
    score: int
    skill: int
    employee: UUID


class AddPetScoreList(Schema):
    items: List[PetScoreDTO]
