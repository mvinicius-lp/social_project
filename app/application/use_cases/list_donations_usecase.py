class ListDonationsUseCase:
    def __init__(self, repo):
        self.repo = repo

    async def execute(self):
        return await self.repo.list_all()
