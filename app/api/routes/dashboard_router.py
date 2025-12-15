from fastapi import APIRouter
from app.application.use_cases.dashboard_usecase import DashboardUseCase

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/")
async def get_dashboard():
    usecase = DashboardUseCase()
    data = await usecase.execute()

    return {
        "totalArrecadado": data["total_arrecadado"],
        "totalDoadores": data["total_doadores"],
        "doacaoMedia": data["doacao_media"],
        "doacoesMes": data["doacoes_mes"]
    }


@router.get("/saldo")
async def get_saldo_disponivel():
    usecase = DashboardUseCase()
    data = await usecase.execute()  # 🔹 AQUI ESTÁ A CORREÇÃO

    return {
        "saldoDisponivel": data["saldo_disponivel"],
        "totalArrecadado": data["total_arrecadado"],
        "totalAplicado": data["total_aplicado"],
    }

@router.get("/charts")
async def get_dashboard_charts():
    usecase = DashboardUseCase()
    return await usecase.get_charts()