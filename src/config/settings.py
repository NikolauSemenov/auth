from datetime import timedelta
from pathlib import Path

from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8080

    project_name: str
    project_version: str

    postgres_dsn: PostgresDsn
    redis_dsn: RedisDsn

    secret_key: str = "SUPER_SECRET_KEY"
    algorithm: str = "HS256"
    access_token_lifetime: timedelta = timedelta(minutes=2)

    @property
    def api_prefix(self) -> str:
        return f"/{self.project_name}/api/{self.project_version}"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
    )


settings = Settings()  # type: ignore
