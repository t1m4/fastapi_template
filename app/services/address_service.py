from app.commands.address_command import (
    BatchCreateAddressCommand,
    BatchUpdateAddressCommand,
)
from app.db.tables.address import Address
from app.schemas.request.address_request import (
    AddressCreateBatchInRequest,
    AddressUpdateBatchInRequest,
)
from app.schemas.response.address_response import (
    AddressCreateBatchResponse,
    AddressUpdateBatchResponse,
)


class BatchCreateAddressService:
    _model = Address

    def __init__(self, *, batch_create_address_command: BatchCreateAddressCommand) -> None:
        self.batch_create_address_command = batch_create_address_command

    async def __call__(self, user_id: int, addresses: AddressCreateBatchInRequest) -> AddressCreateBatchResponse:
        created_addresses = await self.batch_create_address_command.batch_create(user_id, addresses.addresses)
        # created_addresses = await self.batch_create_address_command.batch_create_using_core(
        #     user_id, addresses.addresses
        # )
        return AddressCreateBatchResponse(user_id=user_id, addresses=created_addresses)


class BatchUpdateAddressService:
    _model = Address

    def __init__(self, *, batch_update_address_command: BatchUpdateAddressCommand) -> None:
        self.batch_update_address_command = batch_update_address_command

    async def __call__(self, user_id: int, addresses: AddressUpdateBatchInRequest) -> AddressUpdateBatchResponse:
        updated_addresses = await self.batch_update_address_command.batch_update(user_id, addresses.addresses)
        # updated_addresses = await self.batch_update_address_command.batch_update_with_core(
        #   user_id,
        #   addresses.addresses
        # )
        return AddressUpdateBatchResponse(user_id=user_id, addresses=updated_addresses)
