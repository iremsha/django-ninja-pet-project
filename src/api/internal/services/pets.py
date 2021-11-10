from typing import List

from api.internal.models.pet import Pet
from api.pkg.pagination import paginate
from api.pkg.django import get_object_by_id



class PetService:
    @staticmethod
    def get_pet_by_id(id: int) -> Pet:
        return get_object_by_id(Pet, id=id)


    @staticmethod
    def get_pet_list(limit: int, offset: int) -> (int, List[Pet]):
        pets = Pet.objects.all()

        return pets.count(), paginate(pets, limit, offset)
