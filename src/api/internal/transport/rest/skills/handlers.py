from typing import Optional

from api.internal.dto.skills import AddSkillScoreList
from api.internal.transport.rest.employee.responses import DepartmentListOut, EmployeeShortListOut
from api.internal.service.employee import EmployeeService
from api.internal.service.skills import SkillsService
from api.internal.transport.rest.skills.responses import (
    SkillOut,
    SkillListOut,
    EditSkillIn,
    SkillIn,
    SkillScoreListOut,
    SkillSectionListOut,
    SkillGroupListOut, SkillScoreOut, SkillSectionOut, SkillGroupOut,
)
from api.pkg.responses import SuccessResponse
from api.internal.transport.rest.skills.requests import SkillListQuery, SkillScoreListIn

from ninja import Query


class SkillsHandler:
    def __init__(self, skills_service: SkillsService, employee_service: EmployeeService):
        self.skills_service = skills_service
        self.employee_service = employee_service

    def get_skill_by_id(self, request, id: int) -> SkillOut:
        return self.skills_service.get_skill_by_id(id)

    def delete_skill(self, request, id: int) -> SuccessResponse:
        result = self.skills_service.delete_skill(id)

        return SuccessResponse(success=result)

    def edit_skill(self, request, id: int, edit_skill_data: EditSkillIn) -> SkillOut:
        return self.skills_service.edit_skill(id, edit_skill_data)

    def add_skill(self, request, skill_data: SkillIn) -> SkillOut:
        return self.skills_service.add_skill(skill_data)

    def get_skill_list(self, request, query: SkillListQuery = Query(...)) -> SkillListOut:
        count, skill_list = self.skills_service.get_skill_list(**query.dict())
        return SkillListOut(
            count=count,
            items=[SkillOut.from_orm(skill) for skill in skill_list]
        )

    def add_skill_score_list(self, request, skill_score_list_data: SkillScoreListIn) -> SuccessResponse:
        result = self.skills_service.add_skill_score_list(AddSkillScoreList(**skill_score_list_data.dict()))

        return SuccessResponse(success=result)

    def get_skill_score_list(self, request, query: SkillListQuery = Query(...)) -> SkillScoreListOut:
        count, skill_score_list = self.skills_service.get_skill_score_list(request.user, **query.dict())

        return SkillScoreListOut(
            count=count,
            items=[SkillScoreOut.from_orm(skill_score) for skill_score in skill_score_list]
        )

    def get_employees(self, request) -> EmployeeShortListOut:
        count, employees = self.employee_service.get_employees()
        return EmployeeShortListOut(count=count, employees=employees)

    def get_departments(self, request) -> DepartmentListOut:
        count, departments = self.employee_service.get_departments()
        return DepartmentListOut(count=count, items=departments)

    def get_sections(self, request) -> SkillSectionListOut:
        count, sections = self.skills_service.get_skill_section_list()

        return SkillSectionListOut(
            count=count,
            items=[SkillSectionOut.from_orm(section) for section in sections]
        )

    def get_groups(self, request, section: Optional[int] = Query(default=None)) -> SkillGroupListOut:
        count, groups = self.skills_service.get_skill_group_list(section)
        return SkillGroupListOut(
            count=count,
            items=[SkillGroupOut.from_orm(group) for group in groups]
        )
