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

    secret_key: str
    algorithm: str
    access_token_lifetime: timedelta = timedelta(minutes=20)

    kafka_bootstrap_servers: str = "localhost:29092"
    topic_create_user: str = "user_for_register_events"
    topic_verify_email: str = "verify_email_events"
    ttl_email_code_life: timedelta = timedelta(minutes=3)
    email_secret_code: str

    @property
    def api_prefix(self) -> str:
        return f"/{self.project_name}/api"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
    )


settings = Settings()  # type: ignore
