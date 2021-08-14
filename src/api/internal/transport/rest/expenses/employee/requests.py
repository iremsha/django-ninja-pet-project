from ninja import Schema
from enum import Enum
from typing import Optional


class ExpenseStatusEnum(str, Enum):
    ALL = 'ALL'
    PAID = 'PAID'
    REQUESTED = 'REQUESTED'


class QueryExpensesList(Schema):
    limit: int = 20
    offset: int = 0
    status: ExpenseStatusEnum = ExpenseStatusEnum.ALL.name
