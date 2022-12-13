from http import HTTPStatus

import pytest

from app.config import config
from app.users.handlers import router
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
    url = config.BASE_API_PATH + router.url_path_for("create_user")
    response = client.post(url, json=body)
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
    url = config.BASE_API_PATH + router.url_path_for("get_user", id=str(user.id))

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    json_response = response.json()
    assert json_response == {
        "id": user.id,
        "fullname": user.fullname,
        "info": user.info,
        "created_at": user.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
    }


def test_get_user_does_not_exist(client):
    url = config.BASE_API_PATH + router.url_path_for("get_user", id="1")
    response = client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    json_response = response.json()
    assert json_response == {"message": "User doesn't exists"}


def test_get_users(client):
    user = UserFactory.create()
    url = config.BASE_API_PATH + router.url_path_for("create_user")

    response = client.get(url)
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
    url = config.BASE_API_PATH + router.url_path_for("create_user")

    response = client.get(url, params={"user_ids": user.id})
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
    url = config.BASE_API_PATH + router.url_path_for("get_user", id=str(user.id))
    response = client.put(url, json=body)
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
    url = config.BASE_API_PATH + router.url_path_for("get_user", id="1")
    response = client.put(url, json={"fullname": "test"})
    assert response.status_code == HTTPStatus.NOT_FOUND
    json_response = response.json()
    assert json_response == {"message": "User doesn't exists"}
