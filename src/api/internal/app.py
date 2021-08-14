from ninja import NinjaAPI

from api.internal.router.expenses.employee import add_employee_expenses_routers
from api.internal.router.expenses.admin import add_admin_expenses_routers
from api.internal.router.incomes import add_income_routers
from api.internal.router.employee import add_employee_routers
from api.internal.router.equipment import add_equipment_routers
from api.internal.router.skills import add_skills_routers
from api.internal.router.transfer_money import add_transfer_money_routers
from api.internal.router.project import add_project_routers
from api.internal.router.clients import add_clients_routers

from api.internal.transport.rest.employee.handlers import EmployeeHandler
from api.internal.transport.rest.expenses.employee.handlers import EmployeeExpenseHandler
from api.internal.transport.rest.expenses.admin.handlers import AdminExpenseHandler
from api.internal.transport.rest.incomes.handlers import IncomeHandler
from api.internal.transport.rest.equipment.handlers import EquipmentHandler
from api.internal.transport.rest.skills.handlers import SkillsHandler
from api.internal.transport.rest.transfer_money.handlers import TransferMoneyHandler
from api.internal.transport.rest.project.handlers import ProjectHandler
from api.internal.transport.rest.clients.handlers import ClientHandler

from api.internal.service.toggl import TogglService
from api.internal.service.employee import EmployeeService
from api.internal.service.expenses.salary import SalaryService
from api.internal.service.expenses.sick_leave import SickLeaveService
from api.internal.service.expenses.vacation import VacationService
from api.internal.service.expenses.corporate_expense import CorporateExpenseService
from api.internal.service.expenses.expenses import ExpensesService
from api.internal.service.incomes import IncomeService
from api.internal.service.equipment import EquipmentService
from api.internal.service.skills import SkillsService
from api.internal.service.transfer_money import TransferMoneyService
from api.internal.service.commission import CommissionService
from api.internal.service.project import ProjectService
from api.internal.service.client import ClientService

from api.pkg.errors import HTTPException, ObjectNotFoundException, ServiceException


def get_api():
    api = NinjaAPI()

    @api.exception_handler(HTTPException)
    def service_unavailable(request, exc):
        return api.create_response(
            request,
            {"message": exc.reason},
            status=exc.status,
        )

    @api.exception_handler(ServiceException)
    def service_unavailable(request, exc):
        return api.create_response(
            request,
            {"message": exc.reason},
            status=400,
        )

    @api.exception_handler(ObjectNotFoundException)
    def service_unavailable(request, exc):
        return api.create_response(
            request,
            {"message": f'{exc.name} with id {exc.id} not found'},
            status=404,
        )

    # commissions
    commission_service = CommissionService()

    # employee
    toggl_service = TogglService()
    employee_service = EmployeeService(toggl_service=toggl_service)

    employee_handler = EmployeeHandler(employee_service=employee_service)

    add_employee_routers(api, employee_handler=employee_handler)

    # employee expenses
    salary_service = SalaryService()
    vacation_service = VacationService()
    sick_leave_service = SickLeaveService()
    corporate_expense_service = CorporateExpenseService()
    expenses_service = ExpensesService()
    employee_expense_handler = EmployeeExpenseHandler(
        salary_service=salary_service,
        vacation_service=vacation_service,
        sick_leave_service=sick_leave_service,
        corporate_expense_service=corporate_expense_service,
        expenses_service=expenses_service,
    )

    add_employee_expenses_routers(api, employee_expense_handler=employee_expense_handler)

    # admin expenses
    admin_expense_handler = AdminExpenseHandler(
        corporate_expense_service=corporate_expense_service,
        expenses_service=expenses_service,
        commission_service=commission_service,
    )

    add_admin_expenses_routers(api, admin_expense_handler=admin_expense_handler)

    # incomes
    income_service = IncomeService()
    income_handler = IncomeHandler(income_service=income_service, commission_service=commission_service)

    add_income_routers(api, income_handler)

    # equipment
    equipment_service = EquipmentService()
    equipment_handler = EquipmentHandler(equipment_service=equipment_service)
    add_equipment_routers(api, equipment_handler)

    # skills
    skills_service = SkillsService()
    skills_handler = SkillsHandler(skills_service=skills_service, employee_service=employee_service)
    add_skills_routers(api, skills_handler)

    # transfer money
    transfer_money_service = TransferMoneyService()
    transfer_money_handler = TransferMoneyHandler(
        commission_service=commission_service,
        transfer_money_service=transfer_money_service
    )
    add_transfer_money_routers(api, transfer_money_handler)

    # project
    project_service = ProjectService()
    project_handler = ProjectHandler(project_service=project_service)

    add_project_routers(api, project_handler)

    # clients
    client_service = ClientService()
    client_handler = ClientHandler(client_service=client_service)

    add_clients_routers(api, client_handler)

    return api


ninja_api = get_api()
