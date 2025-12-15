from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.infrastructure.mongodb.donation_repository_impl import DonationRepositoryImpl
from app.application.use_cases.create_donation_usecase import CreateDonationUseCase
from app.application.use_cases.list_donations_usecase import ListDonationsUseCase
from app.infrastructure.mongodb.donor_repository_impl import DonorRepositoryImpl

router = APIRouter(prefix="/donations", tags=["Donations"])

class DonationRequest(BaseModel):
    donor: str
    date: str
    type: str
    description: str = ""
    value: float

@router.post("/")
async def create_donation(body: DonationRequest):
    usecase = CreateDonationUseCase(DonationRepositoryImpl())

    try:
        donation = await usecase.execute(
            donor=body.donor,
            date=body.date,
            type=body.type,
            description=body.description,
            value=body.value,
        )

        return {
            "id": donation.id,
            "donor": donation.donor_email,
            "value": donation.value,
            "date": donation.date.strftime("%d/%m/%Y"),
            "type": donation.type,
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/")
async def list_donations():
    donation_repo = DonationRepositoryImpl()
    donor_repo = DonorRepositoryImpl()
    usecase = ListDonationsUseCase(donation_repo)

    donations = await usecase.execute()
    formatted = []

    for d in donations:

        # -----------------------------
        # FILTRA SOMENTE DOAÇÕES POSITIVAS
        # -----------------------------
        if float(d["value"]) <= 0:
            continue

        donor_email = d["donor_email"]
        donor = await donor_repo.find_by_email(donor_email)
        donor_name = donor.nome if donor else donor_email

        formatted.append({
            "id": d["id"],
            "donor": donor_name,
            "date": d["date"].strftime("%d/%m/%Y"),
            "type": d["type"],
            "description": d.get("description", ""),
            "value": float(d["value"]),
        })

    return formatted
