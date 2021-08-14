from ninja import Schema
from enum import Enum
from typing import Optional, List

from api.internal.dto.expenses.corporate_expense import AdminCreateCorporateExpenseDTO
from api.internal.dto.commissions import AddCommissionDTO


class ExpenseStatusEnum(str, Enum):
    ALL = 'ALL'
    PAID = 'PAID'
    REQUESTED = 'REQUESTED'


class QueryExpensesList(Schema):
    limit: int = 20
    offset: int = 0
    status: ExpenseStatusEnum = ExpenseStatusEnum.ALL.name


class AdminCreateCorporateExpenseIn(AdminCreateCorporateExpenseDTO):
    commissions: List[AddCommissionDTO]


class UpdateCorporateExpenseData(Schema):
    company_account_id: int
    employee_payment_method_id: Optional[int]
