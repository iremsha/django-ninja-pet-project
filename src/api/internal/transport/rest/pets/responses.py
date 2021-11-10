from typing import Optional, List
from ninja import Schema


class PetOut(Schema):
    id: int
    name: str
    address: Optional[str]
    site: Optional[str]
    description: Optional[str]


class PetListOut(Schema):
    count: int
    items: List[PetOut]
