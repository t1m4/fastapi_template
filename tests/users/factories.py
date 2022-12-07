import sqlalchemy as sa
from pydantic_factories import ModelFactory

from app import db
from app.users import models, tables


class UserFactory(ModelFactory[models.User]):
    __model__ = models.User

    @classmethod
    def create(cls, **kwargs) -> models.User:
        instance = cls.build(**kwargs)
        return cls.save(instance)

    @staticmethod
    def save(instance: models.User) -> models.User:
        with db.begin():
            query = sa.insert(tables.User).values(instance.dict()).returning(tables.User)
            row = db.select_one(query)
            return models.User.from_orm(row)

    @classmethod
    def get(cls, user_id: int) -> models.User | None:
        with db.connect():
            row = db.select_one(sa.select(tables.User).where(tables.User.id == user_id))
        return models.User.from_orm(row) if row else None
