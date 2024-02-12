import secrets

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: SecretStr
    use_webhook: bool
    drop_pending_updates: bool
    sqlalchemy_logging: bool

    admin_ids: str

    time_zone: str

    postgres_host: str
    postgres_port: str
    postgres_db: str
    postgres_user: str
    postgres_password: str

    redis_host: str
    redis_port: int
    redis_db: int
    redis_user: str
    redis_password: str

    webhook_base_url: str
    webhook_path: str
    webhook_port: int
    webhook_host: str
    webhook_secret_token: str = Field(default_factory=secrets.token_urlsafe)
    reset_webhook: bool

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8", env_file=".env"
    )

    def build_postgres_dsn(self) -> str:
        return (
            "postgresql+asyncpg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    def build_webhook_url(self) -> str:
        return f"{self.webhook_base_url}{self.webhook_path}"

    def get_admin_ids(self) -> list[int]:
        return [
            int(admin_id)
            for admin_id in self.admin_ids.split(",")
            if admin_id.isdigit()
        ]
