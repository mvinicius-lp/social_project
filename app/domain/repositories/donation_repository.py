from abc import ABC, abstractmethod
from app.domain.entities.donation_entity import Donation

class IDonationRepository(ABC):

    @abstractmethod
    async def create(self, donation: Donation) -> Donation:
        pass

    @abstractmethod
    async def list_all(self):
        pass

