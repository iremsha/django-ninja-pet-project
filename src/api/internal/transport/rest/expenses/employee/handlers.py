from api.internal.dto.expenses.corporate_expense import CreateCorporateExpenseDTO
from api.internal.dto.expenses.salary import CreateSalaryDTO
from api.internal.dto.expenses.sick_leave import CreateSickLeaveDTO
from api.internal.dto.expenses.vacation import CreateVacationDTO

from api.internal.service.expenses.salary import SalaryService
from api.internal.service.expenses.vacation import VacationService
from api.internal.service.expenses.sick_leave import SickLeaveService
from api.internal.service.expenses.corporate_expense import CorporateExpenseService
from api.internal.service.expenses.expenses import ExpensesService

from api.internal.transport.rest.expenses.employee.responses import VacationInfoOut, SickLeaveInfoOut
from api.internal.transport.rest.expenses.responses import ExpenseDTO, ExpensesListWithPaginationDTO
from api.internal.transport.rest.expenses.employee.requests import QueryExpensesList

from ninja import Query


class EmployeeExpenseHandler:
    def __init__(
            self,
            salary_service: SalaryService,
            vacation_service: VacationService,
            sick_leave_service: SickLeaveService,
            corporate_expense_service: CorporateExpenseService,
            expenses_service: ExpensesService,
    ):
        self.salary_service = salary_service
        self.vacation_service = vacation_service
        self.sick_leave_service = sick_leave_service
        self.corporate_expense_service = corporate_expense_service
        self.expenses_service = expenses_service

    def add_salary(self, request, salary_data: CreateSalaryDTO) -> ExpenseDTO:
        return self.salary_service.create_salary(employee=request.user, salary_data=salary_data)

    def add_vacation(self, request, vacation_data: CreateVacationDTO) -> ExpenseDTO:
        return self.vacation_service.create_vacation(employee=request.user, vacation_data=vacation_data)

    def get_vacation_info(self, request) -> VacationInfoOut:
        return VacationInfoOut(**self.vacation_service.get_vacation_info(employee=request.user))

    def add_sick_leave(self, request, sick_leave_data: CreateSickLeaveDTO) -> ExpenseDTO:
        return self.sick_leave_service.create_sick_leave(employee=request.user, sick_leave_data=sick_leave_data)

    def get_sick_leave_info(self, request) -> SickLeaveInfoOut:
        return SickLeaveInfoOut(**self.sick_leave_service.get_sick_leave_info(employee=request.user))

    def add_corporate_expense(self, request, corporate_expense_data: CreateCorporateExpenseDTO) -> ExpenseDTO:
        return self.corporate_expense_service.create_corporate_expense(
            employee=request.user,
            corporate_expense_data=corporate_expense_data
        )

    def get_expenses_list(self, request, query: QueryExpensesList = Query(...)) -> ExpensesListWithPaginationDTO:
        return self.expenses_service.get_expenses_list_with_pagination(employee=request.user, **query.dict())
