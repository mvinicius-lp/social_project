from datetime import datetime
from app.domain.entities.donation_entity import Donation
from app.domain.repositories.donation_repository import IDonationRepository
from app.core.database import database

class DonationRepositoryImpl(IDonationRepository):
    def __init__(self):
        self.collection = database["donations"]

    async def create(self, donation: Donation) -> Donation:
        data = donation.dict(exclude={"id"})
        result = await self.collection.insert_one(data)
        donation.id = str(result.inserted_id)
        return donation
    
    async def list_all(self):
        cursor = self.collection.find().sort("date", -1)  
        donations = []

        async for item in cursor:
            item["id"] = str(item["_id"])
            del item["_id"]
            donations.append(item)

        return donations
    
    async def sum_all(self):
        pipeline = [
            {"$group": {"_id": None, "total": {"$sum": "$value"}}}
        ]
        result = await self.collection.aggregate(pipeline).to_list(1)
        return result[0]["total"] if result else 0

    async def count_all(self):
        return await self.collection.count_documents({})

    async def average_value(self):
        pipeline = [
            {"$group": {"_id": None, "avg": {"$avg": "$value"}}}
        ]
        result = await self.collection.aggregate(pipeline).to_list(1)
        return result[0]["avg"] if result else 0

    async def count_donations_current_month(self):
        now = datetime.utcnow()
        first_day = datetime(now.year, now.month, 1)

        return await self.collection.count_documents({
            "date": {"$gte": first_day}
        })

