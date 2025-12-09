from abc import ABC, abstractmethod
from app.domain.entities.donor_entity import Donor

class IDonorRepository(ABC):

    @abstractmethod
    async def create(self, donor: Donor) -> Donor:
        pass

    @abstractmethod
    async def list_all(self) -> list[Donor]:
        pass

    @abstractmethod
    async def delete_by_email(self, email: str) -> bool:
        pass
