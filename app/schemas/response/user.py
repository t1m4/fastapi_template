from pydantic import BaseModel


class UsersList(BaseModel):
    id: int
    first_name: str | None
    last_name: str | None


class UsersListResponse(BaseModel):
    users: list[UsersList]


class UserGetResponse(BaseModel):
    id: int
    first_name: str | None
    last_name: str | None
    email: str
