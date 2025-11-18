from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: Optional[str] = None

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
