from pydantic import BaseModel


class AddressResponse(BaseModel):
    id: int
    email_address: str


class AddressCreateBatchResponse(BaseModel):
    user_id: int
    addresses: list[AddressResponse]


class AddressUpdateBatchResponse(AddressCreateBatchResponse):
    pass
