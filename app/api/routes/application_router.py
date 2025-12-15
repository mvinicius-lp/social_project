from fastapi import APIRouter, HTTPException
from app.infrastructure.mongodb.application_repository_impl import ApplicationRepositoryImpl
from app.infrastructure.mongodb.donor_repository_impl import DonorRepositoryImpl
from app.infrastructure.mongodb.donation_repository_impl import DonationRepositoryImpl
from datetime import datetime

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post("/")
async def create_application(payload: dict):
    donor_repo = DonorRepositoryImpl()
    donation_repo = DonationRepositoryImpl()

    try:
        date = datetime.strptime(payload["date"], "%Y-%m-%d")
        description = payload.get("description", "")
        area = payload.get("area", "")
        donations = payload["donations"]
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Campo ausente: {e}")

    if not donations:
        raise HTTPException(status_code=400, detail="Lista de doações vazia")

    for item in donations:
        donor_name = item["donor"]
        amount = float(item["amount"])

        if amount <= 0:
            raise HTTPException(
                status_code=400,
                detail=f"Valor inválido para o doador {donor_name}"
            )

        donor = await donor_repo.find_by_name(donor_name)
        if not donor:
            raise HTTPException(
                status_code=404,
                detail=f"Doador não encontrado: {donor_name}"
            )

        await donation_repo.create_negative(
            donor_email=donor.email,
            value=amount,  # <-- VALOR REAL
            date=date,
            description=f"Aplicação em {area}: {description}"
        )

    return {
        "success": True,
        "message": "Aplicação registrada com valores reais por doador."
    }

@router.get("/")
async def list_applications():
    donation_repo = DonationRepositoryImpl()
    donor_repo = DonorRepositoryImpl()

    # Traz todas as doações (positivas e negativas)
    donations = await donation_repo.list_all()

    applications = []

    for d in donations:

        # Filtra SOMENTE os negativos (aplicações)
        if float(d["value"]) >= 0:
            continue

        donor = await donor_repo.find_by_email(d["donor_email"])
        donor_name = donor.nome if donor else d["donor_email"]

        applications.append({
            "id": d["id"],
            "date": d["date"],
            "donor": donor_name,
            "area": extract_area_from_description(d.get("description", "")),
            "description": d.get("description", ""),
            "amount": abs(float(d["value"]))  # transformar negativo em positivo
        })

    return applications


def extract_area_from_description(desc: str) -> str:
    """
    Extrai a área do texto "Aplicação em XXX: descrição..."
    Ex: "Aplicação em Alimentação: verduras" -> "Alimentação"
    """
    if desc.startswith("Aplicação em "):
        try:
            return desc.split("Aplicação em ")[1].split(":")[0]
        except:
            return ""
    return ""