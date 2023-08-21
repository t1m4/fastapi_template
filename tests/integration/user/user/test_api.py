from http import HTTPStatus
from fastapi.testclient import TestClient
import pytest
from app.api.api import router


from http import HTTPStatus
from app.config import settings
from app import db
from app.schemas.response.user import UsersList
from tests.factories.user import CreateUserInRequestFactory, UserFactory
from sqlalchemy.ext.asyncio import AsyncEngine

from polyfactory import AsyncPersistenceProtocol, SyncPersistenceProtocol

@pytest.mark.parametrize(
    "test_params",
    [
        {
            'test_name': 'test create user',
            'body': CreateUserInRequestFactory.build().dict()
        }
    ],
)
async def test_create_user(client: TestClient, test_params: dict):
    """GIVEN User body for user create"""
    url = router.url_path_for("create_user")
    # WHEN creating user 
    response = client.post(url, json=test_params['body'])
    assert response.status_code == HTTPStatus.OK
    json_response = response.json()
    # THEN create response data 
    assert isinstance(json_response["id"], int)
    for field, value in test_params['body'].items():
        assert value == json_response.get(field)

    # THEN create response data 
    db_user = await UserFactory.get(json_response["id"])
    json_db_user = db_user.dict()
    for field, value in test_params['body'].items():
        assert value == json_db_user.get(field)


async def test_get_user(client: TestClient):
    """GIVEN Existing User in db"""
    user = await UserFactory.create_async()
    url = router.url_path_for("get_user", user_id=user.id)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    json_response = response.json()
    assert json_response == {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }


async def test_get_user_does_not_exist(client: TestClient):
    url = router.url_path_for("get_user", user_id="1")
    response = client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    json_response = response.json()
    assert json_response == {"detail": "Not Found"}


async def test_get_users(client: TestClient):
    """GIVEN Three different users"""
    users = await UserFactory.create_batch_async(size=3)
    users_by_id = {user.id: user for user in users}
    url = router.url_path_for("create_user")
    # WHEN get list of users
    response = client.get(url)
    # WHEN compare actual users and users from db
    assert response.status_code == HTTPStatus.OK
    json_response = response.json()
    assert json_response.get('users') is not None
    assert len(json_response['users']) == len(users)

    for actual_user in json_response['users']:
        expected_user = users_by_id.get(actual_user['id'])
        for field_name in UsersList.__fields__.keys():
            assert getattr(expected_user, field_name) == actual_user[field_name]
