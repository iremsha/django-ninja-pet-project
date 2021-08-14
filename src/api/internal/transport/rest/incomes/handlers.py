from ninja import Query

from api.internal.dto.commissions import AddCommissionDTO
from api.internal.service.incomes import IncomeService
from api.internal.service.commission import CommissionService
from api.internal.transport.rest.incomes.requests import ClientIncomeIn, OtherIncomeIn
from api.internal.transport.rest.incomes.responses import (
    IncomeCategoryListOut,
    ClientIncomeOut,
    OtherIncomeOut,
    IncomeListOut,
    ShortIncomeOut,
)
from api.internal.dto.incomes import AddClientIncomeDTO, AddOtherIncomeDTO
from api.pkg.requests import PaginationIn


class IncomeHandler:
    def __init__(self, income_service: IncomeService, commission_service: CommissionService):
        self.income_service = income_service
        self.commission_service = commission_service

    def get_client_income(self, request, id: int) -> ClientIncomeOut:
        income = self.income_service.get_client_income(id)
        commissions = self.commission_service.get_commissions(source_income=income)
        return ClientIncomeOut(income=income, commissions=commissions)

    def add_client_income(self, request, income_data: ClientIncomeIn) -> ClientIncomeOut:
        income_data = income_data.dict()
        commissions = income_data.pop('commissions')
        client_income = self.income_service.add_client_income(AddClientIncomeDTO(**income_data))
        commissions = self.commission_service.add_commissions(
            commissions_data=[AddCommissionDTO(**commission) for commission in commissions],
            source_date=client_income.date,
            source_income=client_income
        )

        return ClientIncomeOut(income=client_income, commissions=commissions)

    def get_other_income(self, request, id: int) -> OtherIncomeOut:
        income = self.income_service.get_other_income(id)
        commissions = self.commission_service.get_commissions(source_income=income)
        return OtherIncomeOut(income=income, commissions=commissions)

    def add_other_income(self, request, income_data: OtherIncomeIn) -> OtherIncomeOut:
        income_data = income_data.dict()
        commissions = income_data.pop('commissions')
        other_income = self.income_service.add_other_income(AddOtherIncomeDTO(**income_data))
        commissions = self.commission_service.add_commissions(
            commissions_data=[AddCommissionDTO(**commission) for commission in commissions],
            source_date=other_income.date,
            source_income=other_income
        )

        return OtherIncomeOut(income=other_income, commissions=commissions)

    def get_incomes_list(self, request, pagination_data: PaginationIn = Query(...)) -> IncomeListOut:
        count, income_list = self.income_service.get_incomes_list(**pagination_data.dict())
        return IncomeListOut(count=count, items=[ShortIncomeOut(income) for income in income_list])

    def get_other_income_categories(self, request) -> IncomeCategoryListOut:
        return IncomeCategoryListOut(items=self.income_service.get_other_income_categories())
