def paginate(queryset, limit: int, offset: int):
    return list(queryset[offset:offset+limit])
