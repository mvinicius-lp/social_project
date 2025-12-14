from app.infrastructure.mongodb.donation_repository_impl import DonationRepositoryImpl
from app.infrastructure.mongodb.donor_repository_impl import DonorRepositoryImpl

class DashboardUseCase:
    def __init__(self):
        self.donation_repo = DonationRepositoryImpl()
        self.donor_repo = DonorRepositoryImpl()

    async def execute(self):
        total_arrecadado = await self.donation_repo.sum_all()
        total_doadores = await self.donor_repo.count_all()
        media = await self.donation_repo.average_value()
        doacoes_mes = await self.donation_repo.count_donations_current_month()

        return {
            "total_arrecadado": total_arrecadado,
            "total_doadores": total_doadores,
            "doacao_media": media,
            "doacoes_mes": doacoes_mes
        }
