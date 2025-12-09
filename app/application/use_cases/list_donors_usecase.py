from app.domain.repositories.donor_repository import IDonorRepository

class ListDonorsUseCase:
    def __init__(self, repo: IDonorRepository):
        self.repo = repo

    async def execute(self):
        return await self.repo.list_all()
