from http import HTTPStatus

import pytest

from tests.users.constants import USER_API, USERS_API
from tests.users.factories import UserFactory


@pytest.mark.parametrize(
    "body,expected",
    [
        (
            {"fullname": "test1"},
            {"fullname": "test1", "info": {}},
        ),
        (
            {"fullname": "test2", "info": {"test_2": "test_2"}},
            {"fullname": "test2", "info": {"test_2": "test_2"}},
        ),
    ],
)
def test_create_user(client, body, expected):
    response = client.post(USERS_API, json=body)
    assert response.status_code == HTTPStatus.OK
    json_response = response.json()
    assert isinstance(json_response["id"], int)
    for field, value in expected.items():
        assert value == json_response.get(field)

    db_user = UserFactory.get(json_response["id"])
    json_db_user = db_user.dict()
    for field, value in expected.items():
        assert value == json_db_user.get(field)


def test_get_user(client):
    user = UserFactory.create()

    response = client.get(USER_API.format(id=user.id))
    assert response.status_code == HTTPStatus.OK
    json_response = response.json()
    assert json_response == {
        "id": user.id,
        "fullname": user.fullname,
        "info": user.info,
        "created_at": user.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
    }


def test_get_user_does_not_exist(client):
    response = client.get(USER_API.format(id=1))
    assert response.status_code == HTTPStatus.NOT_FOUND
    json_response = response.json()
    assert json_response == {"message": "User doesn't exists"}


def test_get_users(client):
    user = UserFactory.create()

    response = client.get(USERS_API)
    assert response.status_code == HTTPStatus.OK
    json_response = response.json()
    assert json_response == {
        "users": [
            {
                "id": user.id,
                "fullname": user.fullname,
                "info": user.info,
                "created_at": user.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
            }
        ]
    }


def test_get_users_with_ids(client):
    user = UserFactory.create()

    response = client.get(USERS_API, params={"user_ids": user.id})
    assert response.status_code == HTTPStatus.OK
    json_response = response.json()
    assert json_response == {
        "users": [
            {
                "id": user.id,
                "fullname": user.fullname,
                "info": user.info,
                "created_at": user.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
            }
        ]
    }


@pytest.mark.parametrize(
    "body,expected",
    [
        ({"fullname": "updated"}, {"fullname": "updated", "info": {}}),
        (
            {"fullname": "updated", "info": {"update_info": "update_info"}},
            {"fullname": "updated", "info": {"update_info": "update_info"}},
        ),
    ],
)
def test_update_user(client, body, expected):
    user = UserFactory.create()
    response = client.put(USER_API.format(id=user.id), json=body)
    assert response.status_code == HTTPStatus.OK
    json_response = response.json()
    assert isinstance(json_response["id"], int)
    for field, value in expected.items():
        assert value == json_response.get(field)

    db_user = UserFactory.get(json_response["id"])
    json_db_user = db_user.dict()
    for field, value in expected.items():
        assert value == json_db_user.get(field)


def test_update_user_with_exception(
    client,
):
    response = client.put(USER_API.format(id=1), json={"fullname": "test"})
    assert response.status_code == HTTPStatus.NOT_FOUND
    json_response = response.json()
    assert json_response == {"message": "User doesn't exists"}
