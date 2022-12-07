from pydantic import BaseSettings, Field


class Config(BaseSettings):
    APP_TITLE: str = Field("template")
    ENVIRONMENT: str = Field(...)
    BASE_API_PATH: str = "/api"
    DATABASE_URL: str = Field(...)


config = Config(_env_file=".env", _env_file_encoding="utf-8")  # type: ignore
