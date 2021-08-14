from typing import Optional
from uuid import UUID

from app.domain.pets import PetDTO, CreatePetIn
from app.infrastructure.repositories.pets_repository import PetsRepository


class PetsController:
    def __init__(self, pets_repo: PetsRepository):
        self._pets_repo = pets_repo

    def get_pet_by_id(self, id: UUID) -> Optional[PetDTO]:
        return self._pets_repo.get_pet_by_id(id)

    def create_pet(self, pet: CreatePetIn) -> Optional[PetDTO]:
        return self._pets_repo.create_pet(pet)
