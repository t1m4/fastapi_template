from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.containers import Container
from app.schemas.request.address_request import (
    AddressCreateBatchInRequest,
    AddressUpdateBatchInRequest,
)
from app.schemas.response.address_response import (
    AddressCreateBatchResponse,
    AddressUpdateBatchResponse,
)
from app.services.address_service import (
    BatchCreateAddressService,
    BatchUpdateAddressService,
)

router = APIRouter(prefix='/v1/users/{user_id}/addresses')


@router.post('/', response_model=AddressCreateBatchResponse)
@inject
async def create_batch_addresses(
    user_id: int,
    body: AddressCreateBatchInRequest,
    batch_create_address_service: BatchCreateAddressService = Depends(Provide[Container.batch_create_address_service]),
) -> AddressCreateBatchResponse:
    return await batch_create_address_service(user_id, body)


@router.put('/', response_model=AddressUpdateBatchResponse)
@inject
async def update_batch_addresses(
    user_id: int,
    body: AddressUpdateBatchInRequest,
    batch_update_address_service: BatchUpdateAddressService = Depends(Provide[Container.batch_update_address_service]),
) -> AddressUpdateBatchResponse:
    return await batch_update_address_service(user_id, body)
