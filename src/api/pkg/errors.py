class HTTPException(Exception):
    def __init__(self, status, reason):
        super().__init__()
        self.status = status
        self.reason = reason


class ServiceException(Exception):
    def __init__(self, reason):
        super().__init__()
        self.reason = reason


class ObjectNotFoundException(Exception):
    def __init__(self, name, id):
        super().__init__()
        self.name = name
        self.id = id
