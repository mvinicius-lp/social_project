from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Donation(BaseModel):
    id: Optional[str] = None
    donor_email: str
    date: datetime
    type: str
    description: Optional[str] = ""
    value: float
    created_at: datetime = datetime.utcnow()
