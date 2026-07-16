import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = 'FastAPI Shop'
    debug: bool = True

    database_url: str = Field(
        default='postgresql+asyncpg://user:password@localhost:5432/shop',
        validation_alias='DATABASE_URL',
    )

    cors_origins: list[str] = Field(default_factory=lambda: [
        'http://localhost:5173',
        'http://localhost:3000',
        'http://127.0.0.1:5173',
        'http://127.0.0.1:3000',
    ])

    static_dir: str = 'static'
    images_dir: str = 'static/images'

    # --- Session ---
    session_ttl_minutes: int = 60 * 24
    session_extend_minutes: int = 60 * 24 * 7
    session_rolling_interval_minutes: int = 10
    session_absolute_timeout_days: int = 30

    session_cookie_name: str = "session_id"
    session_cookie_secure: bool = not debug
    session_cookie_domain: str | None = None

    access_cookie_name: str = 'access_token'
    refresh_cookie_name: str = 'refresh_token'

    model_config = SettingsConfigDict(
        env_file=os.getenv('ENV_FILE', '.env'),
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore',
    )


settings = Settings()
print('DATABASE =', settings.database_url)

