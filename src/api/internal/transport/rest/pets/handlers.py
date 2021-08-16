from ninja import Query

from api.internal.services.pets import PetService
from api.internal.transport.rest.pets.responses import PetListOut, PetOut
from api.pkg.requests import PaginationIn


class ClientHandler:
    def __init__(self, client_service: PetService):
        self.client_service = client_service

    def get_client_list(self, request, pagination_data: PaginationIn = Query(...)) -> PetListOut:
        count, clients = self.client_service.get_client_list(**pagination_data.dict())

        return PetListOut(count=count, items=[PetOut.from_orm(client) for client in clients])
