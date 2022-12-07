from datetime import datetime
from typing import Dict

from pydantic import BaseModel


class UserBase(BaseModel):
    fullname: str
    info: Dict = {}


class UserCreate(UserBase):
    ...


class UserUpdate(UserBase):
    ...


class User(UserBase):
    id: int
    created_at: datetime = datetime.now()

    class Config:
        orm_mode = True


class Users(BaseModel):
    users: list[User]
