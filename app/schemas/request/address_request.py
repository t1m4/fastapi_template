from pydantic import BaseModel


class AddressCreateRequest(BaseModel):
    email_address: str


class AddressUpdateRequest(AddressCreateRequest):
    id: int


class AddressCreateBatchInRequest(BaseModel):
    addresses: list[AddressCreateRequest]


class AddressUpdateBatchInRequest(BaseModel):
    addresses: list[AddressUpdateRequest]
