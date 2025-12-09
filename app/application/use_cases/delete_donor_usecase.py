class DeleteDonorUseCase:
    def __init__(self, repo):
        self.repo = repo

    async def execute(self, email: str) -> bool:
        deleted = await self.repo.delete_by_email(email)
        return deleted
