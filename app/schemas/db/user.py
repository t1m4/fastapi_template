from pydantic import BaseModel


class UserDB(BaseModel):
    id: int
    email: str
    is_active: bool
    first_name: str | None
    last_name: str | None

    class Config:
        orm_mode = True
