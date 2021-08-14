from datetime import date
from typing import Optional
from uuid import UUID

from ninja import Schema
from pydantic import validator


class PetDTO(Schema):
    id: UUID
    name: str
    birth_date: date

    class Config:
        title = 'Pet'


class CreatePetIn(Schema):
    name: str
    birth_date: date

    @validator('name')
    def name_non_empty(cls, val):
        if not val:
            raise ValueError('name must be nonempty')

        return val

    class Config:
        title = 'CreatePetRequest'


class CreatePetOut(Schema):
    id: Optional[UUID]
    success: bool

    class Config:
        title = 'CreatePetResponse'
