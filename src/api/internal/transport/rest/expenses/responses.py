from api.internal.models.expenses import Expense
from api.types import CurrencyEnum
from datetime import date
from ninja import Schema
from typing import List


class ExpenseDTO(Schema):
    id: int
    amount: float
    category: str
    currency: CurrencyEnum
    date: date

    def __init__(self, expense: Expense, category: str):
        super().__init__(
            id=expense.id,
            amount=expense.amount,
            currency=expense.currency,
            date=expense.date,
            category=category,
        )


class ExpensesListDTO(Schema):
    __root__: List[ExpenseDTO]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]


class ExpensesListWithPaginationDTO(Schema):
    count: int
    items: ExpensesListDTO

    def __init__(self, count, **kwargs):
        super().__init__(
            count=count,
            **kwargs,
        )
