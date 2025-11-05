from app.domain.entities.user_entity import User
from app.domain.repositories.user_repository import IUserRepository
from app.core.database import database

class UserRepositoryImpl(IUserRepository):
    def __init__(self):
        self.collection = database["users"]

    async def create(self, user: User) -> User:
        user_dict = user.dict()
        result = await self.collection.insert_one(user_dict)
        user.id = str(result.inserted_id)
        return user

    async def find_by_email(self, email: str):
        user_data = await self.collection.find_one({"email": email})
        return User(**user_data) if user_data else None
