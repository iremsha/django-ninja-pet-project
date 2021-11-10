
from ninja import NinjaAPI, Router
from api.internal.transport.rest.pets.handlers import PetHandler
from api.internal.transport.rest.pets.responses import PetListOut


def get_pets_router(client_handler: PetHandler):
    router = Router(tags=['pets'])
    router.add_api_operation('/pets', ['GET'], client_handler.get_client_list, response=PetListOut)

    return router


def add_pets_routers(api: NinjaAPI, client_handler: PetHandler):
    client_router = get_pets_router(client_handler)
    api.add_router('', client_router)

    return api
