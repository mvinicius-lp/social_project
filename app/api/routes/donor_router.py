from fastapi import APIRouter
from pydantic import BaseModel
from app.infrastructure.mongodb.donor_repository_impl import DonorRepositoryImpl
from app.application.use_cases.register_donor_usecase import RegisterDonorUseCase
from app.application.use_cases.list_donors_usecase import ListDonorsUseCase
from app.application.use_cases.delete_donor_usecase import DeleteDonorUseCase

router = APIRouter(prefix="/donors", tags=["Donors"])


# Modelo para receber JSON no body
class DonorCreateRequest(BaseModel):
    nome: str
    email: str
    telefone: str
    endereco: str = ""
    obs: str = ""


@router.post("/")
async def register_donor(body: DonorCreateRequest):
    repo = DonorRepositoryImpl()
    usecase = RegisterDonorUseCase(repo)

    donor = await usecase.execute(
        body.nome,
        body.email,
        body.telefone,
        body.endereco,
        body.obs
    )

    return {"id": donor.id, "nome": donor.nome, "created_at": donor.created_at}


@router.get("/")
async def list_donors():
    repo = DonorRepositoryImpl()
    usecase = ListDonorsUseCase(repo)

    donors = await usecase.execute()

    return [
        {
            "id": d.id,
            "nome": d.nome,
            "email": d.email,
            "telefone": d.telefone,
            "created_at": d.created_at.strftime("%d/%m/%Y"),
            "total": "0,00",
            "ultima": "—",
        }
        for d in donors
    ]

@router.delete("/{email}")
async def delete_donor(email: str):
    repo = DonorRepositoryImpl()
    usecase = DeleteDonorUseCase(repo)

    success = await usecase.execute(email)

    if not success:
        return {"deleted": False, "message": "Doador não encontrado"}

    return {"deleted": True, "message": "Doador removido com sucesso"}