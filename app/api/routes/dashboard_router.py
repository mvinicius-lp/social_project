from fastapi import APIRouter
from app.application.use_cases.dashboard_usecase import DashboardUseCase

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/")
async def get_dashboard():
    usecase = DashboardUseCase()
    data = await usecase.execute()

    return {
        "totalArrecadado": f"R$ {data['total_arrecadado']:.2f}",
        "totalDoadores": data["total_doadores"],
        "doacaoMedia": f"R$ {data['doacao_media']:.2f}",
        "doacoesMes": data["doacoes_mes"]
    }
