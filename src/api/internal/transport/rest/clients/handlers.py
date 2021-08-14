from ninja import Query

from api.internal.service.client import ClientService
from api.internal.transport.rest.clients.responses import ClientListOut, ClientOut
from api.pkg.requests import PaginationIn


class ClientHandler:
    def __init__(self, client_service: ClientService):
        self.client_service = client_service

    def get_client_list(self, request, pagination_data: PaginationIn = Query(...)) -> ClientListOut:
        count, clients = self.client_service.get_client_list(**pagination_data.dict())

        return ClientListOut(count=count, items=[ClientOut.from_orm(client) for client in clients])
