from typing import List

import sqlalchemy

from app import db
from app.users import models, tables


def insert_user(user: models.UserCreate) -> models.User:
    query = sqlalchemy.insert(tables.User).values(fullname=user.fullname, info=user.info).returning(tables.User)
    row = db.select_one(query)
    return models.User.from_orm(row)


def select_user(user_id: int) -> models.User | None:
    query = sqlalchemy.select(tables.User).where(tables.User.id == user_id)
    row = db.select_one(query)
    return models.User.from_orm(row) if row else None


def select_users(user_ids: List[int]) -> List[models.User]:
    if user_ids:
        query = sqlalchemy.select(tables.User).where(tables.User.id.in_(user_ids))
    else:
        query = sqlalchemy.select(tables.User).limit(10)
    rows = db.select_all(query)
    return [models.User.from_orm(row) for row in rows]


def update_user(user_id: int, user: models.UserUpdate) -> models.User | None:
    query = sqlalchemy.update(tables.User).values(**user.dict()).where(tables.User.id == user_id).returning(tables.User)
    row = db.select_one(query)
    return models.User.from_orm(row) if row else None
