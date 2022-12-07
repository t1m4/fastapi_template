from typing import List

from fastapi import APIRouter, Path, Query

from app import db
from app.users import models, services

router = APIRouter()


@router.post(path="/users", response_model=models.User)
def create_user(user: models.UserCreate) -> models.User:
    with db.begin():
        created_user = services.create_user(user)
    return created_user


@router.get(path="/users/{id}", response_model=models.User)
def get_user(
    id_: int = Path(..., alias="id"),
):
    with db.connect():
        user = services.get_user(id_)
    return user


@router.get(path="/users", response_model=models.Users)
def get_users(user_ids: List[int] = Query([])):
    with db.connect():
        users = services.get_users(user_ids)
    return models.Users(users=users)


@router.put(path="/users/{id}", response_model=models.User)
def update_user(*, id_: int = Path(..., alias="id"), user: models.UserUpdate) -> models.User:
    with db.begin():
        updated_user = services.update_user(id_, user)
    return updated_user
