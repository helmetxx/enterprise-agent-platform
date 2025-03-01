from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None

class UserCreate(UserBase):
    email: EmailStr
    password: str
    full_name: str
    is_superuser: bool = False

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool = True

    class Config:
        orm_mode = True

class UserInDB(User):
    hashed_password: str 