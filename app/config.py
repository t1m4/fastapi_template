from typing import Any

from pydantic import BaseSettings, Field, PostgresDsn, RedisDsn, validator


class Config(BaseSettings):
    APP_TITLE: str = Field('template')
    ENVIRONMENT: str = Field(...)
    BASE_API_PATH: str = '/api'

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
    def build_database_url(self, database_url: str | None, values: dict[str, Any]) -> str:
        if isinstance(database_url, str):
            return database_url
        return PostgresDsn.build(
            scheme='postgresql',
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_HOST'),
            port=values.get('POSTGRES_PORT'),
            path=f'/{values.get("POSTGRES_DB")}',
        )

    @validator('REDIS_URL', pre=True)
    def build_redis_url(self, redis_url: str | None, values: dict[str, Any]) -> str:
        if isinstance(redis_url, str):
            return redis_url
        return RedisDsn.build(
            scheme='redis',
            host=values.get('REDIS_HOST'),
            port=values.get('REDIS_PORT'),
            path=f"/{values.get('REDIS_DB')}",
        )


config = Config(_env_file='.env', _env_file_encoding='utf-8')
