from pydantic import BaseModel


class AddressDB(BaseModel):
    id: int
    email_address: str
    user_id: int

    class Config:
        orm_mode = True
