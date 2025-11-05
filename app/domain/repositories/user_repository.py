from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.user_entity import User

class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        pass
