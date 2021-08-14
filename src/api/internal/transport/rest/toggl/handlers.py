# import json
# import calendar
#
# from django.http import JsonResponse
# from django.db.models import Sum, Q
# from django.core.exceptions import PermissionDenied
# from api.utils.errors import handler403, error_response, not_valid_response, toggl_projects_error_response
# from api.internal.models.employee import Employee, ChangesSalary
# from api.internal.models.project import Project
# from api.internal.models.toggl import TogglRecord
# from api.internal.service import toggl_service
# from api.internal.service.toggl import Toggl
# from api.models import SalaryExpense
# from api.auth.views import AuthenticatedView
# from .requests import TogglRequestForm, TogglDataForm
# from .responses import serialize_toggl_report
# from api.pkg.date import get_str_month
#
#
# class TogglView(AuthenticatedView):
#     def post(self, request):
#         data = request.body or '{}'
#         toggle_request_form = TogglRequestForm(json.loads(data))
#
#         if not toggle_request_form.is_valid():
#             return not_valid_response(toggle_request_form.errors)
#
#         month = get_str_month(toggle_request_form.cleaned_data['month'])
#         year = str(toggle_request_form.cleaned_data['year'])
#
#         # find employee
#         try:
#             employee = Employee.objects.get(id=toggle_request_form.cleaned_data['employee_id'])
#         except Employee.DoesNotExist:
#             return error_response('employee_not_found', 'Сотрудник не найден.')
#
#         if not request.user.is_superuser and not request.user.id == employee.id:
#             return handler403(request, PermissionDenied)
#         return self.create_toggl_records(employee, year, month)
#
#     @staticmethod
#     def create_toggl_records(employee, year, month):
#         _, last_mont_day = calendar.monthrange(int(year), int(month))
#
#         # get employee's Toggl settings
#         toggle_data_form = TogglDataForm(
#             dict(
#                 toggl_email=employee.toggl_email,
#                 toggl_workspace_ids=employee.toggl_workspace_ids,
#                 toggl_token=employee.toggl_token,
#             )
#         )
#
#         if not toggle_data_form.is_valid():
#             return error_response('toggl_not_filled', 'Раздел Toggl в профиле не заполнен.')
#
#         # initialize Toggl
#         toggl = Toggl()
#         toggl.setAPIKey(toggle_data_form.cleaned_data['toggl_token'])
#
#         # Get Toggl profile
#         toggl_user = toggl.getMe()['data']['fullname']
#
#         since = f'{year}-{month}-01'
#         until = f'{year}-{month}-{last_mont_day}'
#         reports = [toggl.getDetailedReport(
#             dict(
#                 user_agent=toggle_data_form.cleaned_data['toggl_email'],
#                 workspace_id=workspace_id,
#                 since=since,
#                 until=until,
#                 grouping='users',
#                 subgrouping='projects',
#             )
#         ) for workspace_id in toggle_data_form.cleaned_data['toggl_workspace_ids']]
#
#         # regroup Toggl report by projects
#         from collections import defaultdict
#         toggl_report_by_projects = dict(
#             total=0,
#             projects=defaultdict(int),
#         )
#         projects_errors = set()
#         employee_rate = TogglView.get_employee_rate_by_date(employee, year, month)
#         toggl_ids = []
#         for report in reports:
#             for record in report['data']:
#                 if not record['user'] == toggl_user:
#                     continue
#
#                 seconds = record['dur'] / 1000
#                 toggl_report_by_projects['total'] += seconds
#                 project_key = record['project']
#                 try:
#                     project = Project.objects.get(key__iexact=project_key)
#                     toggl_report_by_projects['projects'][project.key] += seconds
#                     toggl_ids.append(record['id'])
#
#                     TogglRecord.objects.update_or_create(
#                         toggl_id=record['id'],
#                         employee=employee,
#                         defaults=dict(
#                             seconds=seconds,
#                             start=record['start'],
#                             rate=employee_rate,
#                             project=project,
#                         )
#                     )
#                 except Project.DoesNotExist:
#                     projects_errors.add(project_key)
#
#         # remove deleted toggl records
#         toggl_service.filter_records_by_date(TogglRecord.objects.all(), since, until)\
#             .exclude(toggl_id__in=toggl_ids).delete()
#
#         if len(projects_errors):
#             return toggl_projects_error_response(list(projects_errors))
#
#         # get employee current month expenses
#         requested_salary = SalaryExpense\
#             .objects\
#             .filter(employee=employee, month=month, year=year)\
#             .aggregate(Sum('amount'))['amount__sum']
#
#         if requested_salary is not None:
#             requested_salary = float(requested_salary)
#         employee_data = dict(rate=float(employee_rate), currency=employee.currency, requested_salary=requested_salary)
#
#         return JsonResponse(serialize_toggl_report(
#             toggl_report_by_projects,
#             employee_data,
#         ))
#
#     @staticmethod
#     def get_employee_rate_by_date(employee, year, month):
#         month = int(month)
#         year = int(year)
#         last_changes = ChangesSalary.objects.filter(employee=employee).filter(
#             (Q(year=year) & Q(month__lte=month)) | Q(year__lt=year)
#         ).order_by('year', 'month')
#
#         if last_changes.exists():
#             return last_changes.last().new_rate
#         return 0
