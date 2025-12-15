from app.core.database import database   

class ApplicationRepositoryImpl:

    def __init__(self):
        self.collection = database["applications"]

    async def create(self, data: dict):
        result = await self.collection.insert_one(data)
        data["id"] = str(result.inserted_id)
        return data

    async def list_all(self):
        apps = await self.collection.find().to_list(None)

        formatted = []
        for a in apps:
            formatted.append({
                "id": str(a["_id"]),
                "date": a["date"],
                "donors": a["donors"],
                "area": a["area"],
                "description": a.get("description", ""),
                "amount": float(a["amount"])
            })

        return formatted

    async def sum_by_donor(self, donor_name: str) -> float:
        pipeline = [
            {"$match": {"donors": donor_name}},
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ]
        agg = await self.collection.aggregate(pipeline).to_list(1)
        return float(agg[0]["total"]) if agg else 0.0
