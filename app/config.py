from typing import Any

from pydantic import BaseSettings, Field, PostgresDsn, RedisDsn, validator
from pydantic.fields import ModelField


class Config(BaseSettings):
    APP_TITLE: str = Field('template')
    DEBUG: bool = False
    LOG_LEVEL: str = Field(...)
    ENVIRONMENT: str = Field(...)

    POSTGRES_HOST: str = Field(...)
    POSTGRES_PORT: str = Field(...)
    POSTGRES_USER: str = Field(...)
    POSTGRES_PASSWORD: str = Field(...)
    POSTGRES_DB: str = Field(...)
    DATABASE_URL: PostgresDsn | None = None

    REDIS_HOST: str = Field(...)
    REDIS_PORT: str = Field(...)
    REDIS_DB: str = Field(...)
    REDIS_URL: RedisDsn | None = None

    SENTRY_DSN: str | None = Field(None)

    @validator('DATABASE_URL', pre=True)
    def build_database_url(
        cls, value: str | None, values: dict[str, Any], config: BaseSettings, field: ModelField  # noqa: N805
    ) -> str:
        if isinstance(value, str):
            return value
        return PostgresDsn.build(
            scheme='postgresql+psycopg',
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_HOST'),
            port=values.get('POSTGRES_PORT'),
            path=f'/{values.get("POSTGRES_DB")}',
        )

    @validator('REDIS_URL', pre=True)
    def build_redis_url(
        cls, value: str | None, values: dict[str, Any], config: BaseSettings, field: ModelField  # noqa: N805
    ) -> str:
        if isinstance(value, str):
            return value
        return RedisDsn.build(
            scheme='redis',
            host=values.get('REDIS_HOST'),
            port=values.get('REDIS_PORT'),
            path=f"/{values.get('REDIS_DB')}",
        )


settings = Config(_env_file='.env', _env_file_encoding='utf-8')
