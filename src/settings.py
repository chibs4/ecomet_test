from pydantic import validator, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    # Настройки сервера
    PROJECT_NAME: str = "Ecomet test"
    VERSION: str = "1.0.0"
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000

    # Настройки базы
    POSTGRES_SERVER: str = "0.0.0.0"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "repos_db"
    POSTGRES_PORT: int = 5432
    POSTGRES_URI: PostgresDsn = None

    @validator("POSTGRES_URI", pre=True)
    def assemble_database_url(cls, _, values: dict[str, Any]) -> PostgresDsn:
        """Получение URL для postgress"""
        params = dict(
            host=values["POSTGRES_SERVER"],
            port=values["POSTGRES_PORT"],
            username=values["POSTGRES_USER"],
            password=values["POSTGRES_PASSWORD"],
            path=f'{values["POSTGRES_DB"]}',
        )
        return PostgresDsn.build(scheme="postgres", **params)


settings = Settings()
