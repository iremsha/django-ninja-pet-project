from api.internal.dto.commissions import CommissionDTO
from api.internal.dto.payment_methods import PaymentMethodDTO
from api.internal.models.expenses import CommissionExpense
from api.internal.models.incomes import Income, ClientIncome, OtherIncome
from api.internal.transport.rest.clients.responses import ClientOut
from api.internal.transport.rest.project.responses import ProjectShortOut
from api.types import CurrencyEnum
from typing import Optional, List
from datetime import date
from ninja import Schema


class ProjectIncomeOut(Schema):
    id: int
    project: ProjectShortOut
    rate: float
    hours: float


class IncomeOut(Schema):
    id: int
    amount: float
    currency: CurrencyEnum
    date: date
    description: Optional[str] = None
    company_account: PaymentMethodDTO
    commissions: List[CommissionDTO]

    def __init__(self, income: Income, commissions: List[CommissionExpense], **kwargs):
        super().__init__(
            id=income.id,
            amount=income.amount,
            currency=income.currency,
            date=income.date,
            description=income.description,
            company_account=income.source,
            commissions=[CommissionDTO(commission.expense) for commission in commissions],
            **kwargs
        )


class ClientIncomeOut(IncomeOut):
    client: ClientOut
    projects: List[ProjectIncomeOut]

    def __init__(self, income: ClientIncome, commissions: List[CommissionExpense]):
        super().__init__(
            income=income,
            commissions=commissions,
            client=ClientOut.from_orm(income.client),
            projects=[ProjectIncomeOut.from_orm(project_income) for project_income in income.projects.all()]
        )


class IncomeCategoryOut(Schema):
    id: int
    name: str


class OtherIncomeOut(IncomeOut):
    category: IncomeCategoryOut

    def __init__(self, income: OtherIncome, commissions: List[CommissionExpense]):
        super().__init__(
            income=income,
            commissions=commissions,
            category=IncomeCategoryOut.from_orm(income.category),
        )


class IncomeCategoryListOut(Schema):
    items: List[IncomeCategoryOut]

    def __init__(self, items):
        super().__init__(items=[IncomeCategoryOut.from_orm(income_category) for income_category in items])


class ShortIncomeOut(Schema):
    id: int
    amount: float
    currency: CurrencyEnum
    date: date
    description: Optional[str] = None
    company_account: PaymentMethodDTO

    def __init__(self, income: Income):
        super().__init__(
            id=income.id,
            amount=income.amount,
            currency=income.currency,
            date=income.date,
            company_account=income.source,
        )


class IncomeListOut(Schema):
    count: int
    items: List[ShortIncomeOut]
