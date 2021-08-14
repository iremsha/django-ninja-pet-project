from ninja import Schema
from datetime import date
from typing import Optional, List

from api.internal.dto.commissions import CommissionDTO, AddCommissionDTO
from api.types import CurrencyEnum


class ProjectIncomeIn(Schema):
    id: int
    rate: float
    hours: float


class ClientIncomeIn(Schema):
    amount: float
    description: Optional[str]
    client_id: int
    currency: CurrencyEnum
    company_account_id: int
    date: date
    projects: List[ProjectIncomeIn]
    commissions: List[AddCommissionDTO]


class OtherIncomeIn(Schema):
    amount: float
    description: Optional[str]
    category_id: int
    currency: CurrencyEnum
    company_account_id: int
    date: date
    commissions: List[AddCommissionDTO]

