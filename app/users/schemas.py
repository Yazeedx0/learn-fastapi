from pydantic import BaseModel, EmailStr
from uuid import UUID 
from datetime import datetime 



class UserCreate(BaseModel):
    email: EmailStr
    password: str 


class UserRead(BaseModel):

    id: UUID 
    email: EmailStr
    is_activate: bool 
    is_verified: bool 
    role: str 
    create_at: datetime

    class Config: 
        from_attributes: True 
        