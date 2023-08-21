import pytest
from app.api.api import router
from app.schemas.request.address_request import AddressCreateBatchInRequest, AddressUpdateBatchInRequest, AddressUpdateRequest
from app.schemas.response.address_response import AddressCreateBatchResponse, AddressResponse
from tests.factories.address import AddressCreateRequestFactory, AddressFactory
from tests.factories.user import UserFactory
from http import HTTPStatus
from fastapi.testclient import TestClient


async def test_create_batch_addresses(client: TestClient,):
    """GIVEN Created user and several addresses body"""
    user = await UserFactory.create_async()
    addresses = [AddressCreateRequestFactory.build() for _ in range(2)]
    addresses_body = AddressCreateBatchInRequest(addresses=addresses)
    url = router.url_path_for("create_batch_addresses", user_id=user.id)
    # WHEN create addresses
    response = client.post(url, json=addresses_body.dict())
    assert response.status_code == HTTPStatus.OK
    json_response = response.json()
    # THEN check created addresses response
    assert json_response
    assert json_response['user_id'] == user.id
    assert json_response['addresses']
    assert len(json_response['addresses']) == len(addresses)
    for index, response_address in enumerate(json_response['addresses']):
        assert response_address['email_address'] == addresses[index].email_address
        assert response_address['id']
    # THEN check responses and existing dbs
    db_addresses = await AddressFactory.all()
    for index, response_address in enumerate(json_response['addresses']):
        assert response_address['id'] == db_addresses[index].id
        assert response_address['email_address'] == db_addresses[index].email_address
        assert db_addresses[index].user_id == user.id

async def test_update_batch_addresses(client: TestClient):
    """GIVEN Created user and addresses"""
    user = await UserFactory.create_async()
    db_addresses = await AddressFactory.create_batch_async(size=3, user_id=user.id)
    updated_email = 'updated_email'
    addresses = [{'id': db_address.id, 'email_address': updated_email} for db_address in db_addresses]
    addresses_body = AddressUpdateBatchInRequest(addresses=addresses)
    url = router.url_path_for("update_batch_addresses", user_id=user.id)
    # WHEN update addresses
    response = client.put(url, json=addresses_body.dict())
    assert response.status_code == HTTPStatus.OK
    json_response = response.json()
    # THEN check created addresses response
    assert json_response
    assert json_response['user_id'] == user.id
    assert json_response['addresses']
    assert len(json_response['addresses']) == len(addresses)
    for response_address in json_response['addresses']:
        assert response_address['email_address'] == updated_email
        assert response_address['id']
    # THEN check responses and existing dbs
    db_addresses = await AddressFactory.all()
    for index, response_address in enumerate(json_response['addresses']):
        assert response_address['email_address'] == db_addresses[index].email_address

