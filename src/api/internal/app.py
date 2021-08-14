from ninja import NinjaAPI

from api.internal.router.skills import add_skills_routers
from api.internal.transport.rest.skills.handlers import SkillsHandler


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



    # admin expenses
    admin_expense_handler = AdminExpenseHandler(
        corporate_expense_service=corporate_expense_service,
        expenses_service=expenses_service,
        commission_service=commission_service,
    )

    add_admin_expenses_routers(api, admin_expense_handler=admin_expense_handler)


    # skills
    skills_service = SkillsService()
    skills_handler = SkillsHandler(skills_service=skills_service, employee_service=employee_service)
    add_skills_routers(api, skills_handler)



ninja_api = get_api()
