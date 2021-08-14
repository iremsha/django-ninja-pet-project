from datetime import datetime


def compare_months(date1, date2):
    if date1.year != date2.year:
        return False
    return date1.month == date2.month


def compare_years(date1, date2):
    return date1.year == date2.year


def current_year():
    return datetime.now().year


def current_month():
    return datetime.now().month
