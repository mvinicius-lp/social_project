from typing import Optional
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: str | None = None
    name: str
    email: EmailStr
    password: str
    funcao: Optional[str] = None