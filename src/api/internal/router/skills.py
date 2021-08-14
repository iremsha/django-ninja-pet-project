from ninja import NinjaAPI, Router

from api.internal.transport.rest.skills.handlers import SkillsHandler
from api.internal.transport.rest.skills.responses import SkillOut


def get_skills_router(skills_handler: SkillsHandler):
    router = Router(tags=['skills'])
    router.add_api_operation('/skills/{id}', ['GET'], skills_handler.get_skill_by_id, response=SkillOut)

    router.add_api_operation('/skills', ['POST'], skills_handler.add_skill, response=SkillOut)
    return router


def add_skills_routers(api: NinjaAPI, skills_handler: SkillsHandler):
    skills_router = get_skills_router(skills_handler)
    api.add_router('/', skills_router)

    return api
