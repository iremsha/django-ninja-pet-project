from typing import Optional, List
from ninja import Schema


class ClientOut(Schema):
    id: int
    name: str
    address: Optional[str]
    site: Optional[str]
    description: Optional[str]


class ClientListOut(Schema):
    count: int
    items: List[ClientOut]
