from __future__ import absolute_import, unicode_literals

import logging
import time
from datetime import datetime

from celery import shared_task
from django.db.models import Sum, F
from api.utils.datetime import current_month, current_year
# from api.internal.transport.rest.toggl.handlers import TogglView, get_str_month
from api.models import CompanyAccount, Expense, TransferMoney
from api.internal.models.incomes import Income
from api.internal.models.project import Employee
from api.vacation import VacationDays, VacationMoney
from api.utils.datetime import compare_months, compare_years


@shared_task
def deposit_vacation_days():
    for employee in Employee.objects.all():
        now = datetime.now()

        if employee.vacation_deposited_at and compare_months(employee.vacation_deposited_at, now):
            continue

        previous_month_vacation_days = VacationDays.get_previous_month_vacation_days(employee)

        employee.vacation_days += previous_month_vacation_days
        employee.vacation_deposited_at = now
        employee.save()

        logging.info(f'deposited vacation {previous_month_vacation_days} days to {employee}')


@shared_task
def counting_money_in_company_accounts():
    for company_account in CompanyAccount.objects.all():
        expense_sum = Expense.objects.filter(source=company_account).aggregate(Sum('amount'))['amount__sum'] or 0
        logging.info(f'{company_account} expense_sum {expense_sum}')

        income_sum = Income.objects.filter(source=company_account).aggregate(Sum('amount'))['amount__sum'] or 0
        logging.info(f'{company_account} income_sum {income_sum}')

        transfer_sum_out = TransferMoney.objects.filter(where_from=company_account).aggregate(Sum('amount'))['amount__sum'] or 0
        logging.info(f' {company_account} transfer_sum_out {transfer_sum_out}')

        transfer_sum_in = TransferMoney.objects.filter(where_to=company_account).aggregate(amount__sum=Sum(F('amount') * F('conversion_rate')))['amount__sum'] or 0
        logging.info(f' {company_account} transfer_sum_in {transfer_sum_in}')

        company_account.amount = income_sum - expense_sum + transfer_sum_in - transfer_sum_out
        company_account.save()

        logging.info(f'Update {company_account} amount to {company_account.amount}')


@shared_task
def update_sick_leave_balance():
    for employee in Employee.objects.all():
        now = datetime.now()

        if employee.sick_leave_balance_deposited_at and compare_years(employee.sick_leave_balance_deposited_at, now):
            continue

        employee.sick_leave_balance = 10 * VacationMoney.get_vacation_day_cost(employee)
        employee.sick_leave_balance_deposited_at = now
        employee.save()

        logging.info(f'Update {employee} sick_leave_balance to {employee.sick_leave_balance}')


# @shared_task
# def update_toggl_records():
#     month = get_str_month(current_month())
#     year = str(current_year())
#     for employee in Employee.objects.all():
#         TogglView.create_toggl_records(employee, year, month)
#         time.sleep(2)
#
#         logging.info(f'Update {employee} toggl records')
