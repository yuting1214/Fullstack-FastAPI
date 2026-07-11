import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "My App"
    APP_VERSION: str = "1.0.0"

    USER_NAME: str = ""
    PASSWORD: str = ""
    SECRET_KEY: str = "change-me-in-production"

    @property
    def DB_URL(self) -> str:
        if self.ENV_MODE == "dev":
            return self.DEV_DB_URL
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return "{}://{}:{}@{}:{}/{}".format(
            self.DB_ENGINE,
            self.DB_USERNAME,
            self.DB_PASS,
            self.DB_HOST,
            self.DB_PORT,
            self.DB_NAME,
        )

    @property
    def ASYNC_DB_URL(self) -> str:
        if self.ENV_MODE == "dev":
            return "sqlite+aiosqlite:///./dev.db"
        if self.DATABASE_URL:
            scheme, rest = self.DATABASE_URL.split("://", 1)
            return f"{scheme}+asyncpg://{rest}"
        return "{}+asyncpg://{}:{}@{}:{}/{}".format(
            self.DB_ENGINE,
            self.DB_USERNAME,
            self.DB_PASS,
            self.DB_HOST,
            self.DB_PORT,
            self.DB_NAME,
        )

    @property
    def API_BASE_URL(self) -> str:
        if self.ENV_MODE == "dev":
            return "http://localhost:5000/"
        return self.HOST_URL


class DevSettings(Settings):
    ENV_MODE: str = "dev"
    DEV_DB_URL: str = "sqlite:///./dev.db"
    model_config = SettingsConfigDict(env_file=".env", extra="allow")


class ProdSettings(Settings):
    ENV_MODE: str = "prod"
    DB_ENGINE: str = ""
    DB_USERNAME: str = ""
    DB_PASS: str = ""
    DB_HOST: str = ""
    DB_PORT: str = ""
    DB_NAME: str = ""
    DATABASE_URL: str = ""
    HOST_URL: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="allow")


def get_settings() -> Settings:
    if os.getenv("ENV_MODE", "dev") == "prod":
        return ProdSettings()
    return DevSettings()


global_settings = get_settings()
