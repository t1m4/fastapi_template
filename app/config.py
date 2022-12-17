from pydantic import BaseSettings, Field, PostgresDsn, RedisDsn


class Config(BaseSettings):
    APP_TITLE: str = Field("template")
    ENVIRONMENT: str = Field(...)
    BASE_API_PATH: str = "/api"
    DATABASE_URL: PostgresDsn = Field(...)
    REDIS_URL: RedisDsn = Field(...)
    SENTRY_DSN: str | None = Field(None)


config = Config(_env_file=".env", _env_file_encoding="utf-8")  # type: ignore
