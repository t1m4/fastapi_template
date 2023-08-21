from pydantic import BaseModel, EmailStr


class CreateUserInRequest(BaseModel):
    first_name: str | None
    last_name: str | None
    email: EmailStr
