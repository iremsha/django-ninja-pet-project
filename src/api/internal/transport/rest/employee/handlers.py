from datetime import date

from api.internal.models.employee import Employee
from api.internal.service.employee import EmployeeService
from api.internal.transport.rest.employee.responses import (
    EmployeeWithPaymentMethodsOut,
    EmployeeTrackedHoursOut,
    EmployeeShortListOut, EmployeePaymentMethodOut, EmployeeShortOut,
)
from api.pkg.errors import HTTPException
from uuid import UUID


class EmployeeHandler:
    def __init__(self, employee_service: EmployeeService):
        self.employee_service = employee_service

    def get_employee_by_id(self, request, id: UUID) -> EmployeeWithPaymentMethodsOut:
        employee = Employee.get_employee_by_id(id)
        if employee is None:
            raise HTTPException(status=404, reason="Employee not found")

        employee_payment_methods = self.employee_service.get_employee_payment_methods(employee=employee)
        employee_payment_methods_dto = [
            EmployeePaymentMethodOut.from_orm(employee_payment_method).dict() for employee_payment_method in
            employee_payment_methods
        ]

        return EmployeeWithPaymentMethodsOut(
            **EmployeeShortOut.from_orm(employee).dict(),
            payment_methods=employee_payment_methods_dto
        )

    def get_employee_tracked_hours(
            self, request, id: UUID, since: date = None, until: date = None
    ) -> EmployeeTrackedHoursOut:
        try:
            return EmployeeTrackedHoursOut(**self.employee_service.get_employee_tracked_hours(id, since, until))
        except Employee.DoesNotExist:
            raise HTTPException(status=404, reason="Employee not found")

    def get_employees(self, request) -> EmployeeShortListOut:
        return self.employee_service.get_employees()
