from ninja import NinjaAPI, Router

from api.internal.transport.rest.employee.responses import EmployeeShortListOut, DepartmentListOut
from api.internal.transport.rest.skills.handlers import SkillsHandler
from api.pkg.responses import SuccessResponse
from api.internal.transport.rest.skills.responses import (
    SkillOut,
    SkillListOut,
    SkillScoreListOut,
    SkillSectionListOut,
    SkillGroupListOut,
)


def get_skills_router(skills_handler: SkillsHandler):
    router = Router(tags=['skills'])

    router.add_api_operation('/skills/score', ['POST'], skills_handler.add_skill_score_list, response=SuccessResponse)
    router.add_api_operation('/skills/score', ['GET'], skills_handler.get_skill_score_list, response=SkillScoreListOut)

    router.add_api_operation('/skills/employees', ['GET'], skills_handler.get_employees, response=EmployeeShortListOut)
    router.add_api_operation('/skills/departments', ['GET'], skills_handler.get_departments, response=DepartmentListOut)
    router.add_api_operation('/skills/sections', ['GET'], skills_handler.get_sections, response=SkillSectionListOut)
    router.add_api_operation('/skills/groups', ['GET'], skills_handler.get_groups, response=SkillGroupListOut)

    router.add_api_operation('/skills/{id}', ['GET'], skills_handler.get_skill_by_id, response=SkillOut)
    router.add_api_operation('/skills/{id}', ['PATCH'], skills_handler.edit_skill, response=SkillOut)
    router.add_api_operation('/skills/{id}', ['DELETE'], skills_handler.delete_skill, response=SuccessResponse)

    router.add_api_operation('/skills', ['POST'], skills_handler.add_skill, response=SkillOut)
    router.add_api_operation('/skills', ['GET'], skills_handler.get_skill_list, response=SkillListOut)

    return router


def add_skills_routers(api: NinjaAPI, skills_handler: SkillsHandler):
    skills_router = get_skills_router(skills_handler)
    api.add_router('/', skills_router)

    return api
