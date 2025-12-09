from app.domain.entities.donor_entity import Donor
from app.domain.repositories.donor_repository import IDonorRepository

class RegisterDonorUseCase:
    def __init__(self, repo: IDonorRepository):
        self.repo = repo

    async def execute(self, nome: str, email: str, telefone: str, endereco: str, obs: str) -> Donor:
        donor = Donor(
            nome=nome,
            email=email,
            telefone=telefone,
            endereco=endereco,
            obs=obs
        )
        return await self.repo.create(donor)
