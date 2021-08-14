from api.internal.models.equipment import Equipment
from ninja import Schema
from ninja.orm import create_schema
from pydantic import validator
from typing import List
from datetime import date
from api.types import BorrowType
from api.utils.photo import get_photo_url


EquipmentModel = create_schema(Equipment, depth=1, exclude=['documents'])


class EquipmentOut(EquipmentModel):
    @validator('qr_code')
    def qr_code_crop(cls, v):
        return get_photo_url(v)


class EquipmentListOut(Schema):
    equipment: List[EquipmentOut]


class BorrowEquipmentIn(Schema):
    borrow_type: BorrowType
    borrow_date: date
    estimated_return_date: date

