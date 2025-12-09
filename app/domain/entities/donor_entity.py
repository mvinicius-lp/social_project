from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Donor(BaseModel):
    id: Optional[str] = None
    nome: str
    email: str
    telefone: str
    endereco: Optional[str] = None
    obs: Optional[str] = None
    created_at: datetime = datetime.utcnow() 
