from ninja import Schema


class PaginationIn(Schema):
    limit: int = 20
    offset: int = 0
