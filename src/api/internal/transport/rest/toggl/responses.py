def serialize_toggl_report(report, employee):
    return dict(
        rate=employee['rate'],
        currency=employee['currency'],
        requested_salary=employee['requested_salary'],
        total_seconds=report['total'],
        records=[dict(
            project=project,
            seconds=seconds,
        ) for project, seconds in report['projects'].items()],
    )
