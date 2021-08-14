from typing import Optional, List

from ninja import Schema

from api.internal.models.expenses import CorporateExpense, CommissionExpense
from api.types import CurrencyEnum
from datetime import date
from api.internal.transport.rest.employee.responses import EmployeeShortOut
from api.internal.dto.payment_methods import PaymentMethodDTO
from api.internal.dto.commissions import CommissionDTO


class AdminCorporateExpenseOut(Schema):
    id: int
    amount: float
    category: str
    currency: CurrencyEnum
    date: date
    description: Optional[str]
    employee: Optional[EmployeeShortOut]
    company_account: PaymentMethodDTO
    commissions: List[CommissionDTO]

    def __init__(self, expense: CorporateExpense, commissions: List[CommissionExpense]):
        super().__init__(
            id=expense.id,
            amount=expense.amount,
            category=expense.category.name,
            currency=expense.currency,
            date=expense.date,
            description=expense.description,
            employee=None if expense.employee is None else EmployeeShortOut.from_orm(expense.employee),
            company_account=expense.source,
            commissions=[CommissionDTO(commission.expense) for commission in commissions],
        )
