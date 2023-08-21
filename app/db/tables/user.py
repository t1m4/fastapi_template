from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import String
from sqlalchemy.orm import Mapped, column_property, mapped_column, relationship

from app.db.tables.address import Address
from app.db.tables.base import Base


class User(Base):
    __tablename__ = 'auth_user'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    first_name: Mapped[str | None] = mapped_column(String(30))
    last_name: Mapped[str | None] = mapped_column(String(30))
    fullname: Mapped[str] = column_property(first_name + ' ' + last_name)
    created_at: Mapped[datetime] = mapped_column(server_default=sa.func.now())
    addresses: Mapped[list[Address]] = relationship(
        'Address',
        back_populates='user',
        cascade='save-update, merge, refresh-expire, expunge, delete, delete-orphan',
    )
