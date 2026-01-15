from typing import List

from pydantic import BaseModel, HttpUrl, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from domain.enums import Environment


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__", env_file=".env", extra='ignore')

    environment: Environment = Environment.production
    debug: bool = False

    db_dsn: PostgresDsn
    db_echo: bool = False

    tz: str = "Europe/Moscow"
    log_level: str = "INFO"

    secret_key: SecretStr
    encrypt_algorithm: str
    access_token_expire_days: int = 1
    refresh_token_expire_days: int = 15

    cors_allow_origins: List[str]
    cors_allow_methods: List[str]

    @property
    def current_db_dsn(self) -> str:
        hosts = self.db_dsn.hosts()[0]

        return f"{self.db_dsn.scheme}://{hosts['username']}:***@{hosts['host']}:{hosts['port']}{self.db_dsn.path}"
