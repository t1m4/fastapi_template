import sqlalchemy as sa
from sqlalchemy import BigInteger, Column, DateTime, Identity, Text
from sqlalchemy.dialects.postgresql import JSONB

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, Identity(), primary_key=True)
    fullname = Column(Text, nullable=False)
    info = Column(JSONB, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=sa.func.now())
