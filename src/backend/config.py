from pydantic import SecretStr
from pydantic_settings import BaseSettings as _BaseSettings
from pydantic_settings import SettingsConfigDict


class BaseSettings(_BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8"
    )


class PostgresConfig(BaseSettings, env_prefix="DB_"):
    host: str
    user: str
    password: SecretStr
    name: str
    port: int

    @property
    def get_dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}"

    @property
    def get_sync_dsn(self) -> str:
        return f"postgresql://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}"


class AppConfig(BaseSettings, env_prefix="APP_"):
    secret_key: SecretStr
    api_version: str = "v1"

    @property
    def api_version_prefix(self):
        return f"/api/{self.api_version.lower()}"


class Config(BaseSettings):
    postgres: PostgresConfig
    appconfig: AppConfig


config = Config(
    postgres=PostgresConfig(),
    appconfig=AppConfig()
)
