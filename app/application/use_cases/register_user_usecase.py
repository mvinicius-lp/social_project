from app.domain.entities.user_entity import User
from app.domain.repositories.user_repository import IUserRepository
from app.core.security import hash_password

class RegisterUserUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def execute(self, name: str, email: str, password: str, funcao: str) -> User:
        existing = await self.repo.find_by_email(email)
        if existing:
            raise ValueError("E-mail já cadastrado.")
        hashed = hash_password(password)
        user = User(name=name, email=email, password=hashed, funcao=funcao)
        return await self.repo.create(user)

