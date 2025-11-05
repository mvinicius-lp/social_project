from fastapi import APIRouter, HTTPException
from app.infrastructure.mongodb.user_repository_impl import UserRepositoryImpl
from app.application.use_cases.register_user_usecase import RegisterUserUseCase
from app.application.use_cases.login_user_usecase import LoginUserUseCase
from app.application.use_cases.logout_user_usecase import LogoutUserUseCase

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(name: str, email: str, password: str):
    repo = UserRepositoryImpl()
    usecase = RegisterUserUseCase(repo)
    try:
        user = await usecase.execute(name, email, password)
        return {"id": user.id, "email": user.email}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(email: str, password: str):
    repo = UserRepositoryImpl()
    usecase = LoginUserUseCase(repo)
    return await usecase.execute(email, password)

@router.post("/logout")
async def logout():
    usecase = LogoutUserUseCase()
    return await usecase.execute()
