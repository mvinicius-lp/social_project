from fastapi import HTTPException, status
from app.domain.repositories.user_repository import IUserRepository
from app.core.security import verify_password, create_access_token

class LoginUserUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def execute(self, email: str, password: str):
        user = await self.repo.find_by_email(email)
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas.")
        token = create_access_token({"sub": user.email})
        return {"access_token": token, "token_type": "bearer"}
