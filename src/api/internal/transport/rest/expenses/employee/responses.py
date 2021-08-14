from ninja import Schema


class VacationInfoOut(Schema):
    vacation_days: int
    vacation_day_cost: float


class SickLeaveInfoOut(Schema):
    sick_leave_balance: int
    sick_leave_day_cost: float
