from app.domain.entities.donation_entity import Donation
from app.infrastructure.mongodb.donor_repository_impl import DonorRepositoryImpl
from app.domain.repositories.donation_repository import IDonationRepository
from datetime import datetime

class CreateDonationUseCase:
    def __init__(self, donation_repo: IDonationRepository):
        self.donation_repo = donation_repo
        self.donor_repo = DonorRepositoryImpl()

    async def execute(self, donor: str, date: str, type: str, description: str, value: float):
        donor_obj = await self.donor_repo.find_by_email(donor)
        if not donor_obj:
            raise ValueError("Doador não encontrado no sistema.")

        donation = Donation(
            donor_email=donor,
            date=datetime.fromisoformat(date),
            type=type,
            description=description,
            value=value,
        )

        return await self.donation_repo.create(donation)
