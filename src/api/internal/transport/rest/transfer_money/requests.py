from ninja import Schema
from datetime import date
from api.internal.dto.commissions import AddCommissionDTO
from typing import List


class TransferMoneyIn(Schema):
    amount: float
    date: date
    conversion_rate: float
    where_to_id: int
    where_from_id: int
    commissions: List[AddCommissionDTO]
