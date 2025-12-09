from app.domain.entities.donor_entity import Donor
from app.domain.repositories.donor_repository import IDonorRepository
from app.core.database import database

class DonorRepositoryImpl(IDonorRepository):
    def __init__(self):
        self.collection = database["donors"]

    async def create(self, donor: Donor) -> Donor:
        donor_dict = donor.dict(exclude={"id"})
        result = await self.collection.insert_one(donor_dict)
        donor.id = str(result.inserted_id)
        return donor

    async def list_all(self):
        cursor = self.collection.find()
        donors = []
        async for item in cursor:
            item["id"] = str(item["_id"])
            del item["_id"]
            donors.append(Donor(**item))
        return donors
    from bson import ObjectId

    async def delete_by_email(self, email: str) -> bool:
        result = await self.collection.delete_one({"email": email})
        return result.deleted_count > 0