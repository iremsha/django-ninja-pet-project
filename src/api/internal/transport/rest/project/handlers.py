from ninja import Query, Path
from api.internal.service.project import ProjectService
from api.internal.transport.rest.project.requests import ProjectHoursIn
from api.internal.transport.rest.project.responses import ProjectListOut, ProjectOut, ProjectHoursOut
from api.pkg.requests import PaginationIn


class ProjectHandler:
    def __init__(self, project_service: ProjectService):
        self.project_service = project_service

    def get_project_list(self, request, pagination_data: PaginationIn = Query(...)) -> ProjectListOut:
        count, projects = self.project_service.get_projects(**pagination_data.dict())
        return ProjectListOut(
            count=count,
            items=[ProjectOut.from_orm(project) for project in projects]
        )

    def get_project_hours(self, request, key: str = Path(...), query_params: ProjectHoursIn = Query(...)) -> ProjectHoursOut:
        return ProjectHoursOut(**self.project_service.get_hours(request.user, key, **query_params.dict()))
