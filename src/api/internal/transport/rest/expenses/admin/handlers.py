from api.internal.dto.commissions import AddCommissionDTO
from api.internal.models.employee import Employee
from api.internal.service.commission import CommissionService
from api.internal.service.expenses.corporate_expense import CorporateExpenseService
from api.internal.service.expenses.expenses import ExpensesService
from api.internal.dto.expenses.expense import ExpenseDTO, ExpensesListWithPaginationDTO
from api.internal.dto.expenses.corporate_expense import CreateCorporateExpenseDTO, AdminCreateCorporateExpenseDTO
from api.internal.transport.rest.expenses.admin.requests import AdminCreateCorporateExpenseIn, \
    UpdateCorporateExpenseData
from api.internal.transport.rest.expenses.admin.responses import AdminCorporateExpenseOut
from api.internal.transport.rest.expenses.employee.requests import QueryExpensesList

from ninja import Query

from api.pkg.errors import ObjectNotFoundException


class AdminExpenseHandler:
    def __init__(
            self,
            corporate_expense_service: CorporateExpenseService,
            expenses_service: ExpensesService,
            commission_service: CommissionService,
    ):
        self.corporate_expense_service = corporate_expense_service
        self.expenses_service = expenses_service
        self.commission_service = commission_service

    def add_corporate_expense(self, request, corporate_expense_data: AdminCreateCorporateExpenseIn) -> ExpenseDTO:
        corporate_expense_data = corporate_expense_data.dict()
        commissions_data = corporate_expense_data.pop('commissions')
        employee = Employee.get_employee_by_id(corporate_expense_data['employee_id'])
        if employee is None:
            raise ObjectNotFoundException(name='Employee', id=corporate_expense_data['employee_id'])

        corporate_expense = self.corporate_expense_service.admin_create_corporate_expense(
            employee=employee,
            corporate_expense_data=AdminCreateCorporateExpenseDTO(**corporate_expense_data)
        )

        commissions = self.commission_service.add_commissions(
            source_date=corporate_expense.date,
            source_expense=self.corporate_expense_service.get_expense_by_id(corporate_expense.id),
            commissions_data=[AddCommissionDTO(**commission) for commission in commissions_data],
        )

        return corporate_expense

    def get_expenses_list(self, request, query: QueryExpensesList = Query(...)) -> ExpensesListWithPaginationDTO:
        return self.expenses_service.get_expenses_list_with_pagination(employee=None, **query.dict())

    def update_expense_by_id(self, request, id: int, update_date: UpdateCorporateExpenseData) -> AdminCorporateExpenseOut:
        corporate_expense = self.corporate_expense_service.update_expense(id, **update_date.dict())
        commissions = self.commission_service.get_commissions(source_expense=corporate_expense)
        return AdminCorporateExpenseOut(
            expense=corporate_expense,
            commissions=commissions
        )

    def get_expense_by_id(self, request, id: int) -> AdminCorporateExpenseOut:
        corporate_expense = self.corporate_expense_service.get_expense_by_id(id)
        commissions = self.commission_service.get_commissions(source_expense=corporate_expense)
        return AdminCorporateExpenseOut(
            expense=corporate_expense,
            commissions=commissions
        )
