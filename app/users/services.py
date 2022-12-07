from typing import List

from app.errors import DoesNotExistsError
from app.users import db, models


def create_user(user: models.UserCreate) -> models.User:
    created_user = db.insert_user(user)
    return created_user


def get_user(user_id: int) -> models.User:
    user = db.select_user(user_id)
    if not user:
        raise DoesNotExistsError("User doesn't exists")
    return user


def get_users(user_ids: List[int]) -> List[models.User]:
    return db.select_users(user_ids)


def update_user(user_id: int, user: models.UserUpdate) -> models.User:
    updated_user = db.update_user(user_id, user)
    if not updated_user:
        raise DoesNotExistsError("User doesn't exists")
    return updated_user
