import math
import calendar
from datetime import datetime, timedelta


def get_str_month(month):
    return str(month) if month >= 10 else f'0{month}'


def get_salary_target_date():
    target_date = datetime.today()
    last_day = calendar.monthrange(target_date.year, target_date.month)[1]
    middle = math.ceil(last_day / 2)
    # В первой половине месяца, значение по умолчанию - предыдущий месяц
    if target_date.day < middle:
        target_date -= timedelta(days=middle)

    return target_date


def get_salary_target_year():
    date = get_salary_target_date()
    return date.strftime('%Y')


def get_salary_target_month():
    date = get_salary_target_date()
    return date.strftime('%m')
